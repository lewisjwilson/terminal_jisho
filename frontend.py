#!/usr/bin/env python3

import os
import re
from itertools import islice
from sql_manager import create_connection, search_sql, select_data

# define an entry object
class Entry:
    def __init__(self, kanji, kana, definition):
        self.kanji = kanji
        self.kana = kana
        self.definition = definition

# clear terminal screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():

    clear()
    results_list = []

    database = r"JMdict_e.db"

    # create a database connection
    conn = create_connection(database)

    with conn:
        filter = input("Word to search: ").strip()+'%'

        if(len(filter) > 1):

            filter = filter+'%'

            # define regex expressions for kanji and kana unicode values
            kanji_filter = bool(re.search(r'[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A\u2E80-\u2FD5]', filter))
            kana_filter = bool(re.search(r'[\u3041-\u3096\u30A0-\u30FF\uFF5F-\uFF9F]', filter))

            if(kanji_filter):
                sql = search_sql('kanji')
            elif(kana_filter):
                sql = search_sql('kana')
            else:
                sql = search_sql('english')

            results_list = select_data(conn, filter, sql)

            firstrow = True
            for row in islice(results_list, 10): # first 10 rows
                if(firstrow):
                    print("\n-------------------------------------------")
                    firstrow = False
                query_results = Entry
                query_results.kanji, query_results.kana, query_results.definition = row
                print(" Kanji: " + query_results.kanji + "\n")
                print(" Kana:  " + query_results.kana + "\n")
                print(" Definition: " + query_results.definition)
                print("-------------------------------------------")

            input("Press Enter to search again...")
            main()

        else:
            input("Exiting... Press Enter to quit...")
            clear()


if __name__ == '__main__':
    main()
