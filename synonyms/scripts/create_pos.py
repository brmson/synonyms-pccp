#!/usr/bin/env python3
from synonyms.part_of_speech.model import POS

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Creates pos model for data")
    parser.add_argument('data', type=str, help='Data')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.data)

    pos = POS.create(args.data)
    pos.save(args.output_file)