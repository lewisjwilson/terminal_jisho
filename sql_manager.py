#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def kanji_search(conn, filter):

    cur = conn.cursor()
    cur.execute("SELECT kanji.value, kana.value, definition.value\
                 FROM kanji \
                 INNER JOIN sense \
                 ON kanji.entry_id = sense.entry_id \
                 INNER JOIN definition \
                 ON sense.id = definition.sense_id \
                 INNER JOIN kana \
                 ON kanji.entry_id = kana.entry_id \
                 WHERE kanji.value LIKE ?", (filter+'%',))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"JMdict_e.db"

    # create a database connection
    conn = create_connection(database)

    with conn:
        filter = input("Word to search: ")
        filter = filter
        kanji_search(conn, filter)


if __name__ == '__main__':
    main()
