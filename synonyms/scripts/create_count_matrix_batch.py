#!/usr/bin/env python3

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, save_mat
from synonyms.ppmi import create_counts, transform, CONTEXT_TYPE
from synonyms.dictionary import Dictionary
import re
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Computes counts and ppmi matrix for given corpus and dictionary")
    parser.add_argument('dictionary', type=str, help='File with saved dictionary')
    parser.add_argument('context_size', type=int, choices=range(1, 4), help='Context size')
    parser.add_argument('context_type', choices=[CONTEXT_TYPE.L, CONTEXT_TYPE.R, CONTEXT_TYPE.LR], help='Context type')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    parser.add_argument('corpuses', type=str, nargs='+', help='Corpus in plain format')
    args = parser.parse_args()
    for corpus in args.corpuses:
        check_input_file_exists(corpus)
    check_input_file_exists(args.dictionary)

    dictionary = Dictionary(filename=args.dictionary)
    regex = re.compile(".*\.([0-9]*)\..*")
    for corpus in args.corpuses:
        number = regex.findall(corpus)[0]
        print('Processing:' + corpus)
        new_filename = args.output_file + '.' + number
        new_dict = dictionary.create_reseted_copy(corpus)

        counts_matrix = create_counts(corpus, new_dict, args.context_size, args.context_type)
        print(counts_matrix.shape)
        new_dict.save(new_filename+'.dict')
        save_mat(counts_matrix, new_filename + '.counts')