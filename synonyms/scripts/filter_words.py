#!/usr/bin/env python3
from synonyms.dictionary import Dictionary
from synonyms.in_out.readers import open_gz

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument('input_file', type=str, help='Input file with corpus in plain text')
    parser.add_argument('dictionary', type=str, help='Input file with dictionary')
    parser.add_argument('output_file', type=str, help='Output file where filtered version of corpus will be stored')
    args = parser.parse_args()
    check_input_file_exists(args.input_file)
    check_input_file_exists(args.dictionary)
    dictionary = Dictionary(filename=args.dictionary)
    with open_gz(args.output_file, 'w+', encoding='utf-8') as w, open_gz(args.input_file, encoding='utf-8') as r:
        for line in r:
            w.write(' '.join([word for word in line.lower().split() if word in dictionary])+'\n')