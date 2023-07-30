# -*- coding: utf-8 -*-
# BudgeTeer
# Projekt von https://github.com/rix1337
# Dieses Modul stellt die SQlite-Datenbank für den BudgeTeer bereit.

import sqlite3
import time

from budgeteer.providers import shared_state


def get_first(iterable):
    return iterable and list(iterable[:1]).pop() or None


def remove_redundant_db_tables(file):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    keep_tables = [
        'BudgeTeer',
        'json',
        'secrets'
    ]

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [row[0] for row in cursor.fetchall()]

    tables_to_drop = set(table_names) - set(keep_tables)

    for table in tables_to_drop:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"Entferne überflüssige Tabelle '{table}' aus der Datenbank.")

    conn.commit()
    cursor.execute("VACUUM")
    conn.close()


class BudgetDB(object):
    def __init__(self, table):
        try:
            self._conn = sqlite3.connect(shared_state.values["dbfile"], check_same_thread=False, timeout=5)
            self._table = table
            if not self._conn.execute(
                    "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = '%s';" % self._table).fetchall():
                self._conn.execute("CREATE TABLE %s (key, value)" % self._table)
                self._conn.commit()
        except sqlite3.OperationalError as e:
            try:
                shared_state.logger.debug(
                    "Fehler bei Zugriff auf BudgeTeer.db: " + str(e) + " (neuer Versuch in 5 Sekunden).")
                time.sleep(5)
                self._conn = sqlite3.connect(shared_state.values["dbfile"], check_same_thread=False, timeout=10)
                self._table = table
                if not self._conn.execute(
                        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = '%s';" % self._table).fetchall():
                    self._conn.execute("CREATE TABLE %s (key, value)" % self._table)
                    self._conn.commit()
                    shared_state.logger.debug("Zugriff auf BudgeTeer.db nach Wartezeit war erfolgreich.")
            except sqlite3.OperationalError as e:
                print("Fehler bei Zugriff auf BudgeTeer.db: ", str(e))

    def count(self):
        res = self._conn.execute("SELECT Count() FROM %s" % self._table).fetchone()
        return res[0] if res else None

    def retrieve(self, key):
        res = self._conn.execute(
            "SELECT value FROM %s WHERE key='%s'" % (self._table, key)).fetchone()
        return res[0] if res else None

    def retrieve_all(self, key):
        res = self._conn.execute(
            "SELECT distinct value FROM %s WHERE key='%s' ORDER BY value" % (self._table, key))
        items = []
        for r in res:
            items.append(str(r[0]))
        return items

    def retrieve_all_beginning_with(self, key):
        res = self._conn.execute(
            "SELECT distinct key FROM " + self._table + " WHERE key LIKE '" + key + "%'")
        items = []
        for r in res:
            items.append(str(r[0]))
        return items

    def retrieve_all_titles(self):
        res = self._conn.execute(
            "SELECT distinct key, value FROM %s ORDER BY key" % self._table)
        items = []
        for r in res:
            items.append([str(r[0]), str(r[1])])
        return items if items else None

    def retrieve_all_titles_unordered(self):
        res = self._conn.execute(
            "SELECT distinct key, value FROM %s" % self._table)
        items = []
        for r in res:
            items.append([str(r[0]), str(r[1])])
        return items if items else None

    def store(self, key, value):
        self._conn.execute("INSERT INTO '%s' VALUES ('%s', '%s')" %
                           (self._table, key, value))
        self._conn.commit()

    def update_store(self, key, value):
        self._conn.execute("DELETE FROM %s WHERE key='%s'" %
                           (self._table, key))
        self._conn.execute("INSERT INTO '%s' VALUES ('%s', '%s')" %
                           (self._table, key, value))
        self._conn.commit()

    def delete(self, key):
        self._conn.execute("DELETE FROM %s WHERE key='%s'" %
                           (self._table, key))
        self._conn.commit()

    def reset(self):
        self._conn.execute("DROP TABLE IF EXISTS %s" % self._table)
        self._conn.commit()

    def rename_table(self, new_name):
        self._conn.execute("ALTER TABLE '%s' RENAME TO '%s'" %
                           (self._table, new_name))
        self._conn.commit()
