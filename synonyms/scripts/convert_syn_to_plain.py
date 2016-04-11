#!/usr/bin/env python3
__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists
from synonyms.corpus.utils import syn2_to_plain


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts syn_v2 corpus in xml format to plain txt format")
    parser.add_argument('input_file', type=str, help='Input file with syn_v2 corpus in xml format')
    parser.add_argument('output_file', type=str, help='Output file where plain version of corpus will be stored')
    parser.add_argument('-k', '--keep-punctuation',
                        dest='keep',
                        action='store_true',
                        default=False,
                        help='Use this switch if you want to keep punctuation')
    parser.add_argument('-t', '--keep-tags',
                        dest='keep_tags',
                        action='store_true',
                        default=False,
                        help='Use this switch if you want to keep tags')
    parser.add_argument('-r', '--raw',
                        dest='raw',
                        action='store_true',
                        default=False,
                        help='Use this switch if you want to keep output raw text')
    args = parser.parse_args()
    check_input_file_exists(args.input_file)
    syn2_to_plain(args.input_file, args.output_file, args.keep, args.keep_tags, args.raw)