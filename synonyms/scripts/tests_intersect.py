#!/usr/bin/env python3
__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists
from synonyms.evaluation.test import Test

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('tests1', type=str, help='File with saved tests1')
    parser.add_argument('tests2', type=str, help='File with saved tests2')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.tests1)
    check_input_file_exists(args.tests2)

    tests1 = Test.load_tests(args.tests1)
    tests2 = Test.load_tests(args.tests2)
    tests = Test.intersect(tests1, tests2)
    Test.save_tests(tests,args.output_file)