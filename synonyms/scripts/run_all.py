#!/usr/bin/env python3

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, save_mat
from synonyms.ppmi import create_counts, transform, CONTEXT_TYPE
from synonyms.dictionary import Dictionary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Computes counts and ppmi matrix for given corpus and dictionary")
    parser.add_argument('corpus', type=str, help='Corpus in plain format')
    parser.add_argument('dictionary', type=str, help='File with saved dictionary')
    parser.add_argument('context_size', type=int, choices=range(1, 4), help='Context size')
    parser.add_argument('context_type', choices=[CONTEXT_TYPE.L, CONTEXT_TYPE.R, CONTEXT_TYPE.LR], help='Context type')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.corpus)
    check_input_file_exists(args.dictionary)

    dictionary = Dictionary(filename=args.dictionary)
    counts_matrix = create_counts(args.corpus, dictionary, args.context_size, args.context_type)
    save_mat(counts_matrix, args.output_file + '.counts')
    ppmi_matrix = transform(counts_matrix, dictionary)
    save_mat(ppmi_matrix, args.output_file + '.ppmi')