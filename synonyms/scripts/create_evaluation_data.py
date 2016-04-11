#!/usr/bin/env python3
__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, load_mat
from synonyms.dictionary import Dictionary
from synonyms.evaluation.test import Test
from synonyms.synonyms import SVDModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('matrix', type=str, help='File containing U and S matrix in npz format')
    parser.add_argument('dictionary', type=str, help='File with saved dictionary')
    parser.add_argument('target_words', type=str, help='File containing targets word, each word on one line')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.matrix)
    check_input_file_exists(args.dictionary)
    check_input_file_exists(args.target_words)

    dictionary = Dictionary(filename=args.dictionary)

    words = []
    with open(args.target_words) as f:
        for line in f:
            words.append(line.strip())

    data = load_mat(args.matrix)
    model = SVDModel(data['U'], data['s'], dictionary, caron_p=0.15, dimensions=2500)
    i = 1
    with open(args.output_file, 'w') as file:
        for target_word in words:
            print("\r word %d" % i)
            synonyms = model.get_synonyms(target_word, 10, return_ids=False)
            file.write("%s : %s\n" % (target_word, " ".join(synonyms)))
            i += 1
