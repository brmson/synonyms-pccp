#!/usr/bin/env python3
from synonyms.in_out.readers import open_gz

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Computes counts and ppmi matrix for given corpus and dictionary")
    parser.add_argument('corpus', type=str, help='Corpus')
    parser.add_argument('word_count', type=int, help='Word count')
    parser.add_argument('postfix_length', type=int)
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.corpus)

    max_count = args.word_count
    with open_gz(args.corpus) as input:
        word_count = 0
        file_count = 0
        line_1 = None
        end_of_file = False
        output = None
        for line in input:
            line = line.strip()
            if not output:
                output = open_gz(args.output_file + ('.%0' + str(args.postfix_length) + 'd') % file_count + '.gz', 'w')
            if line == '\n':
                output.write('\n')
                continue
            words = len(line.split())
            word_count += words
            if line_1:
                output.write(line_1 + '\n')
            if word_count == max_count:
                output.write(line + '\n')
                line = None
                end_of_file = True
            elif word_count > max_count:
                if word_count - max_count < abs(word_count - max_count - words):
                    output.write(line + '\n')
                    line = None
                end_of_file = True
            if end_of_file:
                output.close()
                output = None
                end_of_file = False
                file_count += 1
                word_count = words if line else 0
            line_1 = line