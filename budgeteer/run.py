# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Modul initialisiert die globalen Parameter und starte alle parallel laufenden Threads des BudgeTeers.

import argparse
import logging
import multiprocessing
import signal
import sys
import time

from budgeteer.providers import shared_state
from budgeteer.providers import version
from budgeteer.providers.common_functions import Unbuffered, check_ip, configpath
from budgeteer.providers.config import BudgetConfig
from budgeteer.providers.sqlite_database import remove_redundant_db_tables
from budgeteer.web_interface.web_server import web_server

version = "v." + version.get_version()


def main():
    with multiprocessing.Manager() as manager:
        shared_state_dict = manager.dict()
        shared_state_lock = manager.Lock()
        shared_state.set_state(shared_state_dict, shared_state_lock)

        parser = argparse.ArgumentParser()
        parser.add_argument("--log-level", help="Legt fest, wie genau geloggt wird (INFO, DEBUG)")
        parser.add_argument("--config", help="Legt den Ablageort für Einstellungen und Logs fest")
        parser.add_argument("--port", help="Legt den Port des Webservers fest")
        parser.add_argument("--test_run", action='store_true', help="Intern: Führt einen Testlauf durch")
        parser.add_argument("--docker", action='store_true',
                            help="Intern: Sperre Pfad und Port auf Docker-Standardwerte")
        arguments = parser.parse_args()

        shared_state.set_initial_values(arguments.docker)

        sys.stdout = Unbuffered(sys.stdout)

        print("┌──────────────────────────────────────────────┐")
        print("  BudgeTeer " + version + " von RiX")
        print("  https://github.com/rix1337/BudgeTeer")
        print("└──────────────────────────────────────────────┘")

        if shared_state.values["docker"]:
            config_path = "/config"
        else:
            config_path = configpath(arguments.config)

        shared_state.set_files(config_path)

        print('Nutze das Verzeichnis "' + config_path + '" für Einstellungen/Logs')

        log_level = logging.__dict__[
            arguments.log_level] if arguments.log_level in logging.__dict__ else logging.INFO

        shared_state.update("log_level", log_level)
        shared_state.set_logger()

        budgeteer = BudgetConfig('BudgeTeer')
        port = int(budgeteer.get("port"))
        docker = False
        if shared_state.values["docker"]:
            port = int('2808')
            docker = True
        elif arguments.port:
            port = int(arguments.port)

        if budgeteer.get("prefix"):
            prefix = '/' + budgeteer.get("prefix")
        else:
            prefix = ''
        local_address = 'http://' + check_ip() + ':' + str(port) + prefix
        if not shared_state.values["docker"]:
            print('Der Webserver ist erreichbar unter "' + local_address + '"')

        shared_state.set_connection_info(local_address, port, prefix, docker)

        BudgetConfig("BudgeTeer").remove_redundant_entries()
        remove_redundant_db_tables(shared_state.values["dbfile"])

        if not arguments.test_run:
            process_web_server = multiprocessing.Process(target=web_server,
                                                         args=(shared_state_dict, shared_state_lock,))
            process_web_server.start()
        else:
            print("Testlauf aktiviert, Webserver wird nicht gestartet")
            sys.exit(0)

        def signal_handler(sig, frame):
            process_web_server.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        print('Drücke [Strg] + [C] zum Beenden')
        try:
            while True:
                signal.pause()
        except AttributeError:
            while True:
                time.sleep(1)


if __name__ == "__main__":
    main()
