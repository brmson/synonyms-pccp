__author__ = 'veselt12'
from ..dictionary import Dictionary
from ..evaluation.test import Test
from ..synonyms import SVDModel
from ..in_out.utils import load_mat


def load(matrix_file, tests_file, dictionary_file):
    matrix = load_mat(matrix_file)
    tests = Test.load_tests(tests_file)
    dictionary = Dictionary(dictionary_file)
    return matrix, tests, dictionary


def run():
    data, tests, dictionary = load('10000.1.LR.ppmi.mat.npz', 'test', 'syn2.dict')
    model = SVDModel(data['U'], data['s'], dictionary, caron_p=0.25, dimensions=2500)
    syn_pairs, reg_pairs = create_test_pair(dictionary, tests)
    X, y, weights, words = create_X_y_weights(syn_pairs, reg_pairs, model.matrix, dictionary)
    return X, y, weights, words


def create_test_pair(dictionary, tests):
    synonym_pairs = set()
    regular_pairs = set()
    for test in tests:
        for word in test.correct_words:
            synonym_pairs.add((test.target_word, word))
        random_words = dictionary.random_words(100, set([test.target_word]+test.correct_words))
        for rw in random_words:
            regular_pairs.add((test.target_word, rw))
    return synonym_pairs, regular_pairs


def create_X_y_weights(synonym_pairs, regular_pairs, matrix, dictionary):
    X = []
    y = []
    words = []
    weights = []
    for target, word in synonym_pairs:
        vec = (matrix[dictionary.get_id(target), :]-matrix[dictionary.get_id(word), :]).tolist()
        vec = list(map(abs, vec[0]))
        X.append(vec)
        y.append(1)
        words.append((target, word))
        weights.append(0.5/len(synonym_pairs))

    for target, word in regular_pairs:
        vec = (matrix[dictionary.get_id(target), :]-matrix[dictionary.get_id(word), :]).tolist()
        vec = list(map(abs, vec[0]))
        X.append(vec)
        y.append(0)
        words.append((target, word))
        weights.append(0.5/len(regular_pairs))
    return X, y, weights, words

