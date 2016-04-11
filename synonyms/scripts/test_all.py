#!/usr/bin/env python3
__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, load_mat
from synonyms.dictionary import Dictionary
from synonyms.evaluation.test import Test
from synonyms.synonyms import SVDModel, SVDToOneModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('matrix', type=str, help='File containing U and S matrix in npz format')
    parser.add_argument('dictionary', type=str, help='File with saved dictionary')
    parser.add_argument('tests', type=str, help='File with saved tests')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    parser.add_argument('model', choices=['Normal', 'ToOne'], help='Context type')
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    check_input_file_exists(args.matrix)
    check_input_file_exists(args.dictionary)
    check_input_file_exists(args.tests)

    dictionary = Dictionary(filename=args.dictionary)
    tests = Test.load_tests(args.tests)
    data = load_mat(args.matrix)
    if args.model == 'ToOne':
        model = SVDToOneModel(data['U'], data['s'], dictionary)
    else:
        model = SVDModel(data['U'], data['s'], dictionary)
    with open(args.output_file, 'w') as file:
        if args.model == 'ToOne':
            file.write('# to_one dimensions r_precision ndcg\n')
            for to_one in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
                model.to_one = to_one
                for dimensions in [100]:  # [10000, 8000, 6000, 4000, 2500, 2000, 1000, 500, 200, 100]:
                    model.dimensions = dimensions
                    r_precision, ndcg = Test.run_tests(tests, model, 10, verbose=args.verbose)
                    file.write('%d %d %.3f %.3f\n' % (to_one, dimensions, r_precision, ndcg))
        else:
            file.write('# caron_p dimensions r_precision ndcg\n')
            for caron_p in [0.15, 0.25, 0.35, 0.5, 0.7, 1, 1.2, 1.5, 2]:
                model.caron_p = caron_p
                for dimensions in [2000, 1000, 500, 200, 100]:  # [10000, 8000, 6000, 4000, 2500, 2000, 1000, 500, 200, 100]:
                    model.dimensions = dimensions
                    r_precision, ndcg = Test.run_tests(tests, model, 10, verbose=args.verbose)
                    file.write('%.2f %d %.3f %.3f\n' % (caron_p, dimensions, r_precision, ndcg))