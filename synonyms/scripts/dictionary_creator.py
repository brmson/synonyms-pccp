#!/usr/bin/env python3

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists
from synonyms.dictionary import Dictionary

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Computes counts and ppmi matrix for given corpus and ditionary")
    parser.add_argument('corpus', type=str, help='Corpus in plain format')
    parser.add_argument('-i', '--interactive', dest='interactive', action='store_true',
                        help='Use this switch if you want to select number of occurrence dynamically')
    parser.add_argument('min_occurrence', type=int, help='Minimum number of occurrences')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.corpus)

    min_occurrences = args.min_occurrence
    dictionary = Dictionary(args.corpus, min_occurrence=min_occurrences)
    if args.interactive:
        while True:
            try:
                ccc = dictionary.get_count_for_minimum_occurrences(min_occurrences)
                entities = dictionary.get_missing_entity_count(min_occurrences)
                print("Dictionary size: %d, entity missing %d, with cutoff %d" % (ccc, entities, min_occurrences))
                ii = input('Type new cutoff or press <return> to use current cutoff: ')
                if ii == '':
                    break
                min_occurrences = int(ii)
            except ValueError as e:
                print(e)
                print("Input must be number")
        dictionary.filter(min_occurrences)
    dictionary.save(args.output_file)