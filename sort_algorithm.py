#!/usr/bin/env python3

def sort_algorithm(results_list, kanji_filter, kana_filter):

    # sort list by length of kanji, kana or english
    if(kanji_filter):
        results_list.sort(key=lambda x: len(x[0]))
    elif(kana_filter):
        results_list.sort(key=lambda x: len(x[1]))
    else:
        results_list.sort(key=lambda x: len(x[2]))

    # sort based on commonness
    results_list.sort(key=lambda x: (0 if x[4] is None else len(x[4])), reverse = True) # kanji
    results_list.sort(key=lambda x: (0 if x[3] is None else len(x[3])), reverse = True) # kana

    return results_list
