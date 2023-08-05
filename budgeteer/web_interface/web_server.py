# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Modul stellt den Webserver und sämtliche APIs des BudgeTeers bereit.

import json
import os
import site
import sys
from functools import wraps
from socketserver import ThreadingMixIn
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler

from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes
from bottle import Bottle, abort, redirect, request, static_file, HTTPError

from budgeteer.providers import version, shared_state
from budgeteer.providers.common_functions import Unbuffered
from budgeteer.providers.config import BudgetConfig
from budgeteer.providers.sqlite_database import BudgetDB


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class NoLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        pass


class Server:
    def __init__(self, wsgi_app, listen='127.0.0.1', port=8080):
        self.wsgi_app = wsgi_app
        self.listen = listen
        self.port = port
        self.server = make_server(self.listen, self.port, self.wsgi_app,
                                  ThreadingWSGIServer, handler_class=NoLoggingWSGIRequestHandler)

    def serve_forever(self):
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.shutdown()
            self.server.server_close()


auth_user = False
auth_hash = False
known_hashes = {}


def app_container():
    global auth_user
    global auth_hash
    global known_hashes

    base_dir = './budgeteer'
    if getattr(sys, 'frozen', False):
        base_dir = os.path.join(sys._MEIPASS).replace("\\", "/")
    elif shared_state.values["docker"]:
        static_location = site.getsitepackages()[0]
        base_dir = static_location + "/budgeteer"

    general = BudgetConfig('BudgeTeer')
    if general.get("prefix"):
        prefix = '/' + general.get("prefix")
    else:
        prefix = ''

    app = Bottle()

    config = BudgetConfig('BudgeTeer')
    auth_user = config.get('auth_user')
    auth_hash = config.get('auth_hash')

    def auth_basic(check_func, realm="private", text="Access denied"):
        def decorator(func):
            @wraps(func)
            def wrapper(*a, **ka):
                global auth_user
                global auth_hash
                _config = BudgetConfig('BudgeTeer')
                auth_user = _config.get('auth_user')
                auth_hash = _config.get('auth_hash')
                user, password = request.auth or (None, None)
                if auth_user and auth_hash:
                    if user is None or not check_func(user, password):
                        err = HTTPError(401, text)
                        err.add_header('WWW-Authenticate', 'Basic realm="%s"' % realm)
                        return err
                return func(*a, **ka)

            return wrapper

        return decorator

    def is_authenticated_user(user, password):
        global auth_user
        global auth_hash
        _config = BudgetConfig('BudgeTeer')
        auth_user = _config.get('auth_user')
        auth_hash = _config.get('auth_hash')
        if auth_user and auth_hash:
            if auth_hash and "scrypt|" not in auth_hash:
                salt = get_random_bytes(16).hex()
                key = scrypt(auth_hash, salt, 16, N=2 ** 14, r=8, p=1).hex()
                auth_hash = "scrypt|" + salt + "|" + key
                _config.save("auth_hash", to_str(auth_hash))
            secrets = auth_hash.split("|")
            salt = secrets[1]
            config_hash = secrets[2]
            if password not in known_hashes:
                # Remember the hash for up to three passwords
                if len(known_hashes) > 2:
                    known_hashes.clear()
                sent_hash = scrypt(password, salt, 16, N=2 ** 14, r=8, p=1).hex()
                known_hashes[password] = sent_hash
            else:
                sent_hash = known_hashes[password]
            return user == _config.get("auth_user") and config_hash == sent_hash
        else:
            return True

    @app.get(prefix + '/')
    @auth_basic(is_authenticated_user)
    def catch_all():
        return static_file('index.html', root=base_dir + "/web_interface/vuejs_frontend/dist")

    @app.get('//<url:re:.*>')
    @auth_basic(is_authenticated_user)
    def redirect_double_slash(url):
        redirect_url = '/' + url
        if prefix and prefix not in redirect_url:
            redirect_url = prefix + redirect_url
        return redirect(redirect_url)

    @app.hook('before_request')
    def redirect_without_trailing_slash():
        no_trailing_slash = [
            "/assets/",
            "/favicon.ico",
            ".user.js",
            "/api/version/"
        ]
        if not request.path.endswith('/') and not any(s in request.path for s in no_trailing_slash):
            raise redirect(request.url + '/')

    if prefix:
        @app.get('/')
        @auth_basic(is_authenticated_user)
        def index_prefix():
            return redirect(prefix)

    @app.get(prefix + '/assets/<filename>')
    def static_files(filename):
        return static_file(filename, root=base_dir + "/web_interface/vuejs_frontend/dist/assets")

    @app.get(prefix + '/favicon.ico')
    def static_favicon():
        return static_file('favicon.ico', root=base_dir + "/web_interface/vuejs_frontend/dist/")

    def to_int(i):
        if isinstance(i, bytes):
            i = i.decode()
        i = str(i).strip().replace("None", "")
        return int(i) if i else ""

    def to_str(i):
        return '' if i is None else str(i)

    @app.get(prefix + "/api/settings/")
    @auth_basic(is_authenticated_user)
    def get_settings():
        try:
            general_conf = BudgetConfig('BudgeTeer')
            return {
                "settings": {
                    "general": {
                        "auth_user": general_conf.get("auth_user"),
                        "auth_hash": "",  # This is always empty to not leak password hashes
                        "port": to_int(general_conf.get("port")),
                        "prefix": general_conf.get("prefix"),
                    }
                }
            }
        except:
            return abort(400, "Failed")

    @app.post(prefix + "/api/settings/")
    @auth_basic(is_authenticated_user)
    def post_settings():
        try:
            data = request.json

            section = BudgetConfig("BudgeTeer")
            section.save(
                "auth_user", to_str(data['general']['auth_user']))

            password_hash = data['general']['auth_hash']
            if password_hash and "scrypt|" not in password_hash:
                salt = get_random_bytes(16).hex()
                key = scrypt(password_hash, salt, 16, N=2 ** 14, r=8, p=1).hex()
                password_hash = "scrypt|" + salt + "|" + key
                section.save(
                    "auth_hash", to_str(password_hash))

            section.save("port", to_str(data['general']['port']))
            section.save("prefix", to_str(data['general']['prefix']).lower())

            return "Success"
        except:
            return abort(400, "Failed")

    @app.get(prefix + "/api/json/<name>/")
    @auth_basic(is_authenticated_user)
    def get_json(name):
        try:
            try:
                data = json.loads(BudgetDB("json").retrieve(name))
            except:
                data = []
            return {
                name: data
            }
        except:
            return abort(400, "Failed to load " + name)

    @app.post(prefix + "/api/json/<name>/")
    @auth_basic(is_authenticated_user)
    def post_json(name):
        try:
            data = request.json
            data = json.dumps(data)
            BudgetDB("json").update_store(name, data)
            return "Successfully saved " + name
        except:
            return abort(400, "Failed")

    @app.get(prefix + "/api/version/")
    @auth_basic(is_authenticated_user)
    def get_version():
        try:
            ver = "v." + version.get_version()
            if version.update_check()[0]:
                updateready = True
                updateversion = version.update_check()[1]
                print('Update steht bereit (' + updateversion +
                      ')! Weitere Informationen unter https://github.com/rix1337/BudgeTeer/releases/latest')
            else:
                updateready = False
            return {
                "version": {
                    "ver": ver,
                    "update_ready": updateready,
                    "docker": shared_state.values["docker"]
                }
            }
        except:
            return abort(400, "Failed")

    Server(app, listen='0.0.0.0', port=shared_state.values["port"]).serve_forever()


def start():
    if version.update_check()[0]:
        updateversion = version.update_check()[1]
        print('Update steht bereit (' + updateversion +
              ')! Weitere Informationen unter https://github.com/rix1337/BudgeTeer/releases/latest')

    app_container()


def web_server(shared_state_dict, shared_state_lock):
    sys.stdout = Unbuffered(sys.stdout)

    shared_state.set_state(shared_state_dict, shared_state_lock)
    shared_state.set_logger()

    start()
