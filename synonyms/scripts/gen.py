#!/usr/bin/env python3
from __future__ import with_statement
__author__ = u'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, load_mat
from synonyms.dictionary import Dictionary
from synonyms.evaluation.test import Test
from synonyms.synonyms import SVDModel
from io import open
from scipy.io import mmread

if __name__ == u'__main__':
    parser = argparse.ArgumentParser(description=u'TODO')
    parser.add_argument(u'u', type=unicode, help=u'File ')
    parser.add_argument(u's', type=unicode, help=u'File ')
    parser.add_argument(u'dictionary', type=unicode, help=u'File with saved dictionary')
    parser.add_argument(u'tests', type=unicode, help=u'File with saved tests')
    parser.add_argument(u'output_file', type=unicode, help=u'Name of the output file')
    parser.add_argument(u'--verbose', action=u'store_true', default=False)
    args = parser.parse_args()
    check_input_file_exists(args.s)
    check_input_file_exists(args.u)
    check_input_file_exists(args.dictionary)
    check_input_file_exists(args.tests)

    dictionary = Dictionary(filename=args.dictionary)
    tests = Test.load_tests(args.tests)
    
    with open(args.u) as uu, open(args.s) as ss:
        u = mmread(uu)
        s = mmread(ss)
        model = SVDModel(u, s, dictionary)
        with open(args.output_file, u'w') as file:
            file.write(u'# caron_p dimensions r_precision ndcg\n')
            for caron_p in [0.1, 0.15, 0.2, 0.25, 0.35, 0.5, 0.7, 1, 1.2, 1.5, 2]:
                model.caron_p = caron_p
                for dimensions in [10000, 8000, 6000, 4000, 2500, 2000, 1000, 500, 200, 100]:
                    model.dimensions = dimensions
                    r_precision, ndcg = Test.run_tests(tests, model, 10, verbose=args.verbose)
                    file.write(u'%.2f %d %.3f %.3f\n' % (caron_p, dimensions, r_precision, ndcg))
