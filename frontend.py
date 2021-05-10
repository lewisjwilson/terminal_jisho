#!/usr/bin/env python3

import os
import re
from sql_manager import create_connection, search_sql, select_data


# clear terminal screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():

    clear()

    database = r"JMdict_e.db"

    # create a database connection
    conn = create_connection(database)

    with conn:
        filter = input("Word to search: ").strip()+'%'

        if(len(filter) > 1):

            # define regex expressions for kanji and kana unicode values
            kanji_filter = bool(re.search(r'[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A\u2E80-\u2FD5]', filter))
            kana_filter = bool(re.search(r'[\u3041-\u3096\u30A0-\u30FF\uFF5F-\uFF9F]', filter))

            if(kanji_filter):
                sql = search_sql('kanji')
            elif(kana_filter):
                sql = search_sql('kana')
            else:
                sql = search_sql('english')

            select_data(conn, filter, sql)

        else:
            print("Exiting...")


if __name__ == '__main__':
    main()
