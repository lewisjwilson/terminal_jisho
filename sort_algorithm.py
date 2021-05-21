#!/usr/bin/env python3

import operator

def sort_algorithm(results_list, kanji_filter, kana_filter):

    """# sort list by length of kanji, kana or english
    if(kanji_filter):
        results_list.sort(key=lambda x: len(x[0]))
    elif(kana_filter):
        results_list.sort(key=lambda x: len(x[1]))
    else:
        results_list.sort(key=lambda x: len(x[2]))

    # sort based on commonness
    results_list.sort(key=lambda x: (0 if x[4] is None else len(x[4])), reverse = True) # kanji
    results_list.sort(key=lambda x: (0 if x[3] is None else len(x[3])), reverse = True) # kana
"""
    v_common = ["news1", "ichi1", "spec1", "gai1"]
    uncommon = None

    new_results_list = []
    # converting commonness to number for sorting
    for row in results_list:
        r = list(row)
        if(r[3] in v_common):
            r[3] = 2
        elif(r[3] == uncommon):
            r[3] = 0
        else:
            r[3] = 1

        if(r[4] in v_common):
            r[4] = 2
        elif(r[4] == uncommon):
            r[4] = 0
        else:
            r[4] = 1
        row = tuple(r)
        new_results_list.append(row)

    new_results_list.sort(key = operator.itemgetter(4, 3), reverse = True)
    new_results_list.sort(key=lambda x: len(x[2])) # sorts by descending length

    return new_results_list
