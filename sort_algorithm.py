#!/usr/bin/env python3

import operator

def sort_algorithm(results_list, kanji_filter, kana_filter):

    simplify(results_list)

    # sort list by length of kanji, kana or english
    if(kanji_filter):
        results_list.sort(key=lambda x: len(x[0]))
    elif(kana_filter):
        results_list.sort(key=lambda x: len(x[1]))
    else:
        results_list.sort(key=lambda x: len(x[2]))

    # sort based on commonness
    # first sort by kana commonness, then by kanji commonness
    results_list = sorted(results_list, key=lambda x: (x[4], x[3]), reverse=True)
    return results_list

def simplify(results_list):

    # for the sake of sorting
    # ichi1, spec1 etc. are mapped to 2
    # ichi2, spec2 etc. are mapped to 1
    # None is mapped to 0
    for item in results_list:
        if(item[3] is None):
            item[3] = 0
        elif(item[3].endswith("1")):
            item[3] = 2
        elif(item[3].endswith("2")):
            item[3] = 1
        else:
            item[3] = 0

        if(item[4] is None):
            item[4] = 0
        elif(item[4].endswith("1")):
            item[4] = 2
        elif(item[4].endswith("2")):
            item[4] = 1
        else:
            item[4] = 0

    return results_list
