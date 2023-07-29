# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Modul stellt Funktionen zur Verfügung, die in vielen Modulen benötigt werden.

import os
import socket
import sys


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def check_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 0))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def configpath(configpath):
    pathfile = "BudgeTeer.conf"
    current_path = os.path.dirname(sys.argv[0])
    if configpath:
        f = open(pathfile, "w")
        f.write(configpath)
        f.close()
    elif os.path.exists(pathfile):
        f = open(pathfile, "r")
        configpath = f.readline()
    else:
        print("Wo sollen Einstellungen und Logs abgelegt werden? Leer lassen, um den aktuellen Pfad zu nutzen.")
        configpath = input("Pfad angeben:")
        if len(configpath) > 0:
            f = open(pathfile, "w")
            f.write(configpath)
            f.close()
    if len(configpath) == 0:
        configpath = current_path
        configpath = configpath.replace("\\", "/")
        configpath = configpath[:-1] if configpath.endswith('/') else configpath
        f = open(pathfile, "w")
        f.write(configpath)
        f.close()
    configpath = configpath.replace("\\", "/")
    configpath = configpath[:-1] if configpath.endswith('/') else configpath
    if not os.path.exists(configpath):
        os.makedirs(configpath)
    return configpath
