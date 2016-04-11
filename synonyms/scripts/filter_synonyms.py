# !/usr/bin/env python3
# from __future__ import with_statement
__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, load_mat
from synonyms.dictionary import Dictionary
from io import open
import re

def strip_word(word):
    return word.split('-', 1)[0].split('_')[0].split('`')[0]


def strip_morpho_tags(synonyms_map):
    synonyms_map_stripped = {}
    for target, synonyms in synonyms_map.items():
        synonyms_map_stripped[strip_word(target)] = list(map(strip_word, synonyms))
    return synonyms_map_stripped

_digits = re.compile('\d')

def is_number(word):
    return bool(_digits.search(word))

def remove_numbers(synonyms_map):
    synonyms_map_without_numbers = {}
    for target, synonyms in synonyms_map.items():
        if not is_number(target):
            synonyms_map_without_numbers[target] = [synonym for synonym in synonyms if not is_number(synonym)]
    return synonyms_map_without_numbers


def remove_stop_list(synonyms_map, stop_list):
    synonyms_map_stop_list = {}
    for target, synonyms in synonyms_map.items():
        if target not in stop_list and len(target) > 2:
            synonyms_map_stop_list[target] = [synonym for synonym in synonyms if
                                              synonym not in stop_list and len(synonyms) > 2]
    return synonyms_map_stop_list


def cut(synonyms_map, cutoff):
    synonyms_map_cutoff = {}
    for target, synonyms in synonyms_map.items():
        synonyms_cutoff = []
        for synonym in synonyms:
            if len(synonyms_cutoff) > cutoff:
                break
            if synonym not in synonyms_cutoff and synonym != target:
                synonyms_cutoff.append(synonym)
        if len(synonyms_cutoff) != 0:
            synonyms_map_cutoff[target] = synonyms_cutoff
    return synonyms_map_cutoff


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('synonyms', type=str, help='File ')
    parser.add_argument('stop_list', type=str, help='File ')
    parser.add_argument('dictionary', type=str, help='File with saved dictionary')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    check_input_file_exists(args.synonyms)
    check_input_file_exists(args.stop_list)
    check_input_file_exists(args.dictionary)
    dictionary = Dictionary(filename=args.dictionary)
    dictionary.size()
    dictionary.word2count = {strip_word(word): count for word, count in dictionary.word2count.items()}
    synonyms_map = {}
    with open(args.synonyms) as file:
        for line in file:
            # print(line.split(' : '))
            target, synonyms = line.strip().split(' : ', 1)
            synonyms = synonyms.strip().split(' ')
            synonyms_map[target] = synonyms
    stop_list = set()
    with open(args.stop_list) as file:
        for line in file:
            word = line.strip().lower()
            stop_list.add(word)
    synonyms_map = strip_morpho_tags(synonyms_map)
    synonyms_map = remove_numbers(synonyms_map)
    synonyms_map = remove_stop_list(synonyms_map, stop_list)
    synonyms_map = cut(synonyms_map, 5)
    with open(args.output_file, 'w') as file:
        for target in sorted(synonyms_map.keys(), key=lambda e: dictionary.get_word2count(e), reverse=True):
            if not dictionary.is_entity(target) and not any(
                    list(map(lambda x: dictionary.is_entity(x), synonyms_map[target]))):
                file.write('%s : %s\n' % (target, ' '.join(synonyms_map[target])))
