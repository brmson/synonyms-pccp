#!/usr/bin/env python3
from synonyms.lemmatizer.morphodita import lemmatize

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('corpus', type=str, help='File containing corpus')
    parser.add_argument('output_corpus', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.corpus)
    lemmatize(args.corpus, args.output_corpus)