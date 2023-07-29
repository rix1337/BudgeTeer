# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Modul stellt die Konfiguration für den BudgeTeer bereit.

import base64
import configparser
import string

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad

from budgeteer.providers import shared_state
from budgeteer.providers.sqlite_database import BudgetDB


class BudgetConfig(object):
    _DEFAULT_CONFIG = {
        'BudgeTeer': [
            ("auth_user", "secret", ""),
            ("auth_hash", "secret", ""),
            ("port", "int", "2808"),
            ("prefix", "str", ""),
        ]
    }
    __config__ = []

    def __init__(self, section):
        self._configfile = shared_state.values["configfile"]
        self._section = section
        self._config = configparser.RawConfigParser()
        try:
            self._config.read(self._configfile)
            self._config.has_section(
                self._section) or self._set_default_config(self._section)
            self.__config__ = self._read_config(self._section)
        except configparser.DuplicateSectionError:
            print('Doppelte Sektion in der Konfigurationsdatei.')
            raise
        except:
            print('Ein unbekannter Fehler in der Konfigurationsdatei ist aufgetreten.')
            raise

    def _set_default_config(self, section):
        self._config.add_section(section)
        for (key, key_type, value) in self._DEFAULT_CONFIG[section]:
            self._config.set(section, key, value)
        with open(self._configfile, 'w') as configfile:
            self._config.write(configfile)

    def _get_encryption_params(self):
        crypt_key = BudgetDB('secrets').retrieve("key")
        crypt_iv = BudgetDB('secrets').retrieve("iv")
        if crypt_iv and crypt_key:
            return base64.b64decode(crypt_key), base64.b64decode(crypt_iv)
        else:
            crypt_key = get_random_bytes(32)
            crypt_iv = get_random_bytes(16)
            BudgetDB('secrets').update_store("key", base64.b64encode(crypt_key).decode())
            BudgetDB('secrets').update_store("iv", base64.b64encode(crypt_iv).decode())
            return crypt_key, crypt_iv

    def _set_to_config(self, section, key, value):
        default_value_type = [param[1] for param in self._DEFAULT_CONFIG[section] if param[0] == key]
        if default_value_type and default_value_type[0] == 'secret' and len(value):
            crypt_key, crypt_iv = self._get_encryption_params()
            cipher = AES.new(crypt_key, AES.MODE_CBC, crypt_iv)
            value = base64.b64encode(cipher.encrypt(pad(value.encode(), AES.block_size)))
            value = 'secret|' + value.decode()
        self._config.set(section, key, value)
        with open(self._configfile, 'w') as configfile:
            self._config.write(configfile)

    def _read_config(self, section):
        return [(key, '', self._config.get(section, key)) for key in self._config.options(section)]

    def _get_from_config(self, scope, key):
        res = [param[2] for param in scope if param[0] == key]
        if not res:
            res = [param[2]
                   for param in self._DEFAULT_CONFIG[self._section] if param[0] == key]
        if [param for param in self._DEFAULT_CONFIG[self._section] if param[0] == key and param[1] == 'secret']:
            value = res[0].strip('\'"')
            if value.startswith("secret|"):
                crypt_key, crypt_iv = self._get_encryption_params()
                cipher = AES.new(crypt_key, AES.MODE_CBC, crypt_iv)
                decrypted_payload = cipher.decrypt(base64.b64decode(value[7:])).decode("utf-8").strip()
                final_payload = "".join(filter(lambda c: c in string.printable, decrypted_payload))
                return final_payload
            else:  ## Loaded value is not encrypted, return as is
                if len(value) > 0:
                    self.save(key, value)
                return value
        elif [param for param in self._DEFAULT_CONFIG[self._section] if param[0] == key and param[1] == 'bool']:
            return True if len(res) and res[0].strip('\'"').lower() == 'true' else False
        else:
            return res[0].strip('\'"') if len(res) > 0 else False

    def save(self, key, value):
        self._set_to_config(self._section, key, value)
        return

    def get(self, key):
        return self._get_from_config(self.__config__, key)

    def get_section(self):
        return self._config._sections[self._section]

    def remove_redundant_entries(self):
        for section in self._config.sections():
            if section not in self._DEFAULT_CONFIG:
                self._config.remove_section(section)
                print(f"Entferne überflüssige Sektion '{section}' aus der Konfigurationsdatei.")
            else:
                for option in self._config.options(section):
                    if option not in [param[0] for param in self._DEFAULT_CONFIG[section]]:
                        self._config.remove_option(section, option)
                        print(
                            f"Entferne überflüssige Option '{option}' der Sektion '{section}' aus der Konfigurationsdatei.")
        with open(self._configfile, 'w') as configfile:
            self._config.write(configfile)
