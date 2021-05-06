#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def search_sql(type):
    # type := kanji, kana or english search
    try:
        return{
            'kanji': "SELECT kanji.value, kana.value, definition.value \
                         FROM kanji \
                         INNER JOIN sense \
                         ON kanji.entry_id = sense.entry_id \
                         INNER JOIN definition \
                         ON sense.id = definition.sense_id \
                         INNER JOIN kana \
                         ON kanji.entry_id = kana.entry_id \
                         WHERE kanji.value LIKE ?",
            'kana': "SELECT kanji.value, kana.value, definition.value \
                         FROM kana \
                         INNER JOIN sense \
                         ON kanji.entry_id = sense.entry_id \
                         INNER JOIN definition \
                         ON sense.id = definition.sense_id \
                         INNER JOIN kanji \
                         ON kanji.entry_id = kana.entry_id \
                         WHERE kana.value LIKE ?",
            'english': "SELECT kanji.value, kana.value, definition.value \
                         FROM kanji \
                         INNER JOIN sense \
                         ON kanji.entry_id = sense.entry_id \
                         INNER JOIN definition \
                         ON sense.id = definition.sense_id \
                         INNER JOIN kana \
                         ON kanji.entry_id = kana.entry_id \
                         WHERE definition.value LIKE ?"
        }.get(type)
    except Error as e:
        print("sql_manager.py: type is '" + type
                            + "', should be 'kanji', 'kana' or 'english.'")
        print(e)


def select_data(conn, filter, sql):

    cur = conn.cursor()

    cur.execute(sql, (filter,))

    rows = cur.fetchall()

    for row in rows:
        print(row)
