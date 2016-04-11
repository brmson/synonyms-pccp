#!/usr/bin/env python3
__author__ = 'veselt12'
import argparse, json
from synonyms.in_out.utils import check_input_file_exists
from synonyms.evaluation.test import Test
from synonyms.lemmatizer.file_lemmatizer import lemmatize
from synonyms.dictionary import Dictionary


def merge(AA, BB):
    A = AA['rating']
    B = BB['rating']
    merged = {k: A.get(k, B.get(k)) for k in A.keys() ^ B.keys()}
    merged.update({
        k: {'rel': (A[k]['rel']*A[k]['count']+B[k]['rel']*B[k]['count'])/(A[k]['count']+B[k]['count']),
            'count': (A[k]['count']+B[k]['count'])}
        for k in A.keys() & B.keys()})
    AA['rating'] = merged
    return AA


def filter(rating):
    for word_id, data in rating.items():
        for word, d in data['rating'].items():
            del d['count']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts web log to tests")
    parser.add_argument('web_log', type=str, help='Web log in json')
    parser.add_argument('dictionary', type=str, help='Dictionary file')
    parser.add_argument('output_file', type=str, help='Name of the output file')
    args = parser.parse_args()
    check_input_file_exists(args.web_log)
    check_input_file_exists(args.dictionary)
    dictionary = Dictionary(args.dictionary)
    rating = {}
    antonyms = {}
    with open(args.web_log, encoding='utf-8') as file:
        web_log = json.load(file)
        for entry in web_log:
            word_d = entry['word']
            words = entry['priority']
            type = [x.strip() for x in entry['type'].split(':')]
            words = [x.strip() for x in words.split(':') if x not in [None, " ", ""]]
            entry = {}
            if type[0] in ['rating', 'antonyms']:
                words_sequence = {word: {'rel': rel, 'count': 1} for rel, word in zip(range(len(words), 0, -1), words)}
                entry = {'word': word_d, 'rating': words_sequence}
                if type[0] == 'rating':
                    if word_d in rating:
                        entry = merge(rating[word_d], entry)
                    rating[word_d] = entry
                else:
                    if word_d in antonyms:
                        entry = merge(antonyms[word_d], entry)
                    antonyms[word_d] = entry
    filter(rating)
    filter(antonyms)
    tests = []
    for word_d, entry in rating.items():
        word = entry['word']
        relevance_scores = []
        synonyms = []
        if '_' in word:
            continue
        if any(['_' in word2 for word2 in entry['rating'].keys()]):
            continue
        for word2, item in entry['rating'].items():
            synonyms.append(word2)
            relevance_scores.append(item['rel'])
        tests.append(Test(word, synonyms, relevance_scores))
    words = []
    for test in tests:
        words.append(test.target_word)
        for syn in test.correct_words:
            words.append(syn)
    lemmatized_words = lemmatize(words)
    i = 0
    for test in tests:
        test.target_word = lemmatized_words[i]
        i += 1
        for j in range(len(test.correct_words)):
            test.correct_words[j] = lemmatized_words[i]
            i += 1
    tests = Test.filter(tests, dictionary)
    Test.save_tests(tests, args.output_file)