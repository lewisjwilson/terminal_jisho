#!/usr/bin/env python3

import subprocess
import os
import re
from itertools import islice
from termcolor import colored
from sort_algorithm import sort_algorithm
from sql_manager import create_connection, create_views, search_sql, select_data


# define an entry object
class Entry:
    def __init__(self, kanji, kana, definition, kanacommon, kanjicommon):
        self.kanji = kanji
        self.kana = kana
        self.definition = definition
        self.kanacommon = kanacommon
        self.kanjicommon = kanjicommon


class _GetchUnix:
    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# clear terminal screen
def clear():
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=False)


# print to screen. start, stop are slices to view
def display_data(results_list, start, stop):
    print(" -------------------------------------------")
    for row in islice(results_list, start, stop):
        entry = Entry

        entry.kanji, entry.kana, entry.definition,\
        entry.kanacommon, entry.kanjicommon, entry.part_of_speech = row

        print(" Kanji: " + entry.kanji + "\n")
        print(" Kana:  " + entry.kana + "\n")
        print(" Definition: " + entry.definition + "\n")

        freq = " Frequency: "
        if(entry.kanjicommon == 2):
            freq += " v. common kanji, "
        elif(entry.kanjicommon == 1):
            freq += " common kanji, "
        else:
            freq += " uncommon kanji, "

        if(entry.kanacommon == 2):
            freq += "v. common kana, "
        elif(entry.kanacommon == 1):
            freq += "freq common, "
        else:
            freq += "uncommon kana, "
        print(freq[:-2] + "\n")  # trim final 2 chars from notes

        notes = " Notes: "
        if(entry.part_of_speech is not None):
            notes += entry.part_of_speech
        print(notes)

        print(" -------------------------------------------")

    print(" Showing items " + str(stop) + " of " + str(len(results_list)) + " results.")
    print(" Prev = \'z\', Next = \'m\', Search again = \'Enter\', Quit = \'q\'")

    getch = _GetchUnix()
    feedback = getch()
    if(feedback == "q"):
        clear()
        quit()
    elif(feedback == "\r"):  # enter
        clear()
    elif(feedback == "z") and (start-1 >= 0):
        clear()
        start -= 1
        stop -= 1
        display_data(results_list, start, stop)
    elif(feedback == "m") and (stop < len(results_list)):
        clear()
        start += 1
        stop += 1
        display_data(results_list, start, stop)
    else:
        clear()
        display_data(results_list, start, stop)


def main():

    clear()
    results_list = []
    results_tuples= []
    database = r"JMdict_e.db"

    # create a database connection
    conn = create_connection(database)
    create_views(conn)

    with conn:
        search_filter = "%" + input(" Word to search: ").strip()+"%"

        if(len(search_filter) > 2):

            # define regex expressions for kanji and kana unicode values
            kanji_filter = bool(re.search(r'[\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A\u2E80-\u2FD5]', search_filter))
            kana_filter = bool(re.search(r'[\u3041-\u3096\u30A0-\u30FF\uFF5F-\uFF9F]', search_filter))

            if(kanji_filter):
                sql = search_sql('kanji')
            elif(kana_filter):
                sql = search_sql('kana')
            else:
                sql = search_sql('english')

            results_tuples = select_data(conn, search_filter, sql)

            # convert list of tuples to list of lists for mutability
            results_list = [list(elem) for elem in results_tuples]

            results_list = sort_algorithm(results_list, kanji_filter, kana_filter)

            # define interval for displaying entries (1 entry show)
            start = 0
            stop = 1

            if len(results_list) > 0:
                clear()
                display_data(results_list, start, stop)
            else:
                input(" No results found! Press Enter...")

            main()

        else:
            clear()


if __name__ == '__main__':
    main()
