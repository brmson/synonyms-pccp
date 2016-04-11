from . import metrics
import json
from ..lemmatizer.file_lemmatizer import lemmatize
from itertools import zip_longest


class Test:
    def __init__(self, target_word, correct_words, relevance_scores=None):
        self.target_word = target_word
        self.correct_words = correct_words
        if relevance_scores is None:
            relevance_scores = [1] * len(correct_words)
        self.relevance_scores = relevance_scores

    def __publish(self, synonyms, score, r_precision, ndcg):
        print("****************%s****************" % self.target_word)
        for syn, sc, cor in zip_longest(synonyms, score, self.correct_words, fillvalue=''):
            print("%s %.3f %s" % (syn, sc, cor))
        print("r-prec=%.3f, ndcg=%.3f" % (r_precision, ndcg))
        print("\n\n")

    def test(self, svd_model, k=10, verbose=False):
        synonyms, score = svd_model.get_synonyms(self.target_word, max(k, len(self.correct_words)), return_ids=False,
                                                 return_score=True)
        r_precision = metrics.r_precision(synonyms, self.correct_words)
        syn_relevance = []
        for synonym in synonyms:
            try:
                index = self.correct_words.index(synonym)
                syn_relevance.append(self.relevance_scores[index])
            except ValueError:
                syn_relevance.append(0)
        ndcg = metrics.ndcg(syn_relevance, k)
        if verbose:
            self.__publish(synonyms, score, r_precision, ndcg)
        return r_precision, ndcg

    def __eq__(self, y):
        return self.target_word == y.target_word

    def __hash__(self):
        return self.target_word.__hash__()

    @staticmethod
    def intersect(tests1, tests2):
        return list(set(tests1) ^ set(tests2))


    @staticmethod
    def load_tests(filename):
        tests = []
        with open(filename, encoding='utf-8') as file:
            for line in file:
                item = json.loads(line)
                tests.append(Test(item['target'], item['correct'], item['relevance']))
        return tests

    @staticmethod
    def save_tests(tests, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for test in tests:
                file.write(json.dumps({'target': test.target_word,
                                       'correct': test.correct_words,
                                       'relevance': test.relevance_scores}) + '\n')

    @staticmethod
    def filter(tests, dictionary):
        t2 = []
        for test in tests:
            if all([word in dictionary for word in [test.target_word] + test.correct_words]):
                t2.append(test)
        return t2

    @staticmethod
    def run_tests(tests, svd_model, k, verbose=False):
        r_precision = 0
        ndcg = 0
        for test in tests:
            r, n = test.test(svd_model, k, verbose=verbose)
            r_precision += r
            ndcg += n
        return r_precision / len(tests), ndcg / len(tests)

    @staticmethod
    def lemmatize_tests(tests):
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