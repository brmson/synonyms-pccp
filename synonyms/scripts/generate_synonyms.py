# !/usr/bin/env python3
from __future__ import with_statement

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, load_mat
from synonyms.dictionary import Dictionary
from synonyms.synonyms import SVDModel
from io import open
from scipy.io import mmread
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('matrix', type=str, help='File containing U and S matrix in npz format')
    parser.add_argument('dictionary', type=str, help='File with saved dictionary')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    check_input_file_exists(args.matrix)
    check_input_file_exists(args.dictionary)
    dictionary = Dictionary(filename=args.dictionary)
    # with open(args.u) as uu, open(args.s) as ss:
    # u = mmread(args.u)
    # s = mmread(args.s)

    data = load_mat(args.matrix)
    model = SVDModel(data['U'], data['s'], dictionary)
    with open(args.output_file, 'w') as file:
        model.caron_p = 0.25
        model.dimensions = 400
        count = 0
        for word in dictionary.all_words():
            print("\r %d" % count, end='')
            synonyms, score = model.get_synonyms(word, 10, return_ids=False, return_score=True)
            file.write("%s : %s\n" % (word, ' '.join(synonyms)))
            count += 1