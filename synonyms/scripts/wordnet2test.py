#!/usr/bin/env python3
__author__ = 'vesely'
import argparse
from synonyms.dictionary import Dictionary
from synonyms.in_out.utils import check_input_file_exists
import xml.etree.ElementTree as ET
from synonyms.evaluation.test import Test


def wordnet_test(synsets):
    tests = []
    for synset in synsets:
        target = synset[0]
        synonyms = []
        for s in synset[1:]:
            synonyms.append(s)
        test = Test(target, synonyms)
        tests.append(test)
    return tests


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts web_log to tests")
    parser.add_argument('wordnet_file', type=str, help='Wordnet file')
    parser.add_argument('dictionary', type=str, help='Dictionary file')
    parser.add_argument('output_file', type=str, help='Output file')
    args = parser.parse_args()
    check_input_file_exists(args.wordnet_file)
    check_input_file_exists(args.dictionary)
    dictionary = Dictionary(filename=args.dictionary)
    synsets = []
    with open(args.wordnet_file, encoding='iso-8859-2') as file:
        for line in file:
            if line.startswith('<?'):
                continue
            root = ET.fromstring(line)
            synsets.append([word.text for word in root.findall('./SYNONYM/LITERAL')])
    count = 0
    synsets = list(filter(lambda synset: len(synset) > 1 and all([' ' not in s for s in synset]), synsets))
    tests = wordnet_test(synsets)
    Test.lemmatize_tests(tests)
    tests = Test.filter(tests, dictionary)
    Test.save_tests(tests, args.output_file)