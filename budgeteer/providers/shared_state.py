# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Modul stellt alle globalen Parameter für die verschiedenen parallel laufenden Threads bereit.

import logging
import os
import sys
from logging import handlers

values = {}
lock = None
logger = None


def set_state(manager_dict, manager_lock):
    global values
    global lock
    values = manager_dict
    lock = manager_lock


def update(key, value):
    global values
    global lock
    lock.acquire()
    try:
        values[key] = value
    finally:
        lock.release()


def set_initial_values(docker):
    update("docker", docker)


def set_files(config_path):
    update("configfile", os.path.join(config_path, "BudgeTeer.ini"))
    update("dbfile", os.path.join(config_path, "BudgeTeer.db"))
    update("log_file", os.path.join(config_path, 'BudgeTeer.log'))
    update("log_file_debug", os.path.join(config_path, 'BudgeTeer_DEBUG.log'))


def set_logger():
    global logger

    log_level = values["log_level"]

    logger = logging.getLogger('budgeteer')
    logger.setLevel(log_level)

    console = logging.StreamHandler(stream=sys.stdout)
    log_format = '%(asctime)s - %(message)s'
    formatter = logging.Formatter(log_format)
    console.setLevel(log_level)

    logfile = logging.handlers.RotatingFileHandler(values["log_file"])
    logfile.setFormatter(formatter)
    logfile.setLevel(logging.INFO)

    if not len(logger.handlers):
        logger.addHandler(logfile)
        logger.addHandler(console)

        if log_level == 10:
            logfile_debug = logging.handlers.RotatingFileHandler(values["log_file_debug"])
            logfile_debug.setFormatter(formatter)
            logfile_debug.setLevel(10)
            logger.addHandler(logfile_debug)


def set_connection_info(local_address, port, prefix, docker):
    update("local_address", local_address)
    update("port", port)
    update("prefix", prefix)
    update("docker", docker)
