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


def create_views(conn):

    cur = conn.cursor()
    cur.execute("""CREATE VIEW IF NOT EXISTS v_kana_grouped\
                AS\
                SELECT kana.entry_id, kanji.value AS kanji_value, group_concat(kana.value, ', ') AS kana_value\
                FROM kana\
                INNER JOIN entry\
                ON entry.entry_id = kana.entry_id\
                INNER JOIN kanji\
                ON kanji.entry_id = kana.entry_id\
                GROUP BY kanji.value""")

    cur.execute("""CREATE VIEW IF NOT EXISTS v_kanji_grouped\
                AS\
                SELECT kana.entry_id, group_concat(kanji.value, ', ') AS kanji_value, kana.value AS kana_value\
                FROM kana\
                INNER JOIN entry\
                ON entry.entry_id = kana.entry_id\
                INNER JOIN kanji\
                ON kanji.entry_id = kana.entry_id\
                GROUP BY kanji.entry_id""")


def search_sql(search_type):
    # search_type := kanji, kana or english search
    if(search_type == "kanji"):
        vals = ["kanji", "kana", "kanji.value"]
    elif(search_type == "kana"):
        vals = ["kana", "kanji", "kana.value"]
    else:
        vals = ["kanji", "kana", "definition.value"]

    sql_string = "SELECT group_concat(kanji.value, \", \"), group_concat(kana.value, \", \"), definition.value, kana_common.value, kanji_common.value, part_of_speech.value \
                     FROM " + vals[0] + " \
                     INNER JOIN sense \
                     ON kanji.entry_id = sense.entry_id \
                     INNER JOIN definition \
                     ON sense.id = definition.sense_id \
                     INNER JOIN " + vals[1] + " \
                     ON kanji.entry_id = kana.entry_id \
                     INNER JOIN part_of_speech\
					 ON part_of_speech.sense_id = sense.id\
                     LEFT JOIN kana_common\
                     ON kana.id = kana_common.kana_id\
                     LEFT JOIN kanji_common\
                     ON kanji.id = kanji_common.kanji_id\
                     WHERE " + vals[2] + " LIKE ?\
                     GROUP BY kanji.entry_id"
    return(sql_string)


def select_data(conn, search_filter, sql):

    search_results = []
    cur = conn.cursor()
    cur.execute(sql, (search_filter,))
    rows = cur.fetchall()

    for row in rows:
        search_results.append(row)

    return search_results
