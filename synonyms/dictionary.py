from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from .in_out.readers import open_gz, BlockFileReader, FileReader

__author__ = 'veselt12'
import re, json, itertools
from collections import defaultdict
from random import choice
import copy


class Dictionary:
    regex = re.compile('#dictionary version=(\d+) size=(\d+)')
    current_version = 1

    def __init__(self, filename, min_occurrence=0):
        self.filename = filename
        with open_gz(filename, encoding='utf-8') as f:
            line = f.readline()
        matches = Dictionary.regex.match(line)
        if matches:
            self.computed = True
            self.file_version, self.min_occurrence = matches.groups()
        else:
            self.min_occurrence = min_occurrence
            self.computed = False
        self.loaded = False

    def all_words(self):
        self.__check()
        return self.word2id.keys()

    def all_ids(self):
        self.__check()
        return self.id2word.keys()

    def __reset(self):
        self.__word_count = 0
        self.word2id = {}
        self.word2count = {}
        self.id2count = {}
        self.id2word = {}

    def __update_dict(self, word, id, count):
        self.word2id[word] = id
        self.word2count[word] = count
        self.id2word[id] = word
        self.id2count[id] = count
        self.__word_count += count

    def save(self, filename):
        self.__check()
        if not filename.endswith('.dict'):
            filename += '.dict'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("#dictionary version=%d size=%d\n" % (Dictionary.current_version, len(self.word2id)))
            file.write("#id word count\n")
            for word in self.word2id.keys():
                file.write("%s %s %s\n" % (self.word2id[word], word, self.word2count[word]))

    def load_computed(self):
        with open(self.filename, encoding='utf-8') as file:
            self.__reset()
            for line in file:
                if line.startswith("#"):
                    continue
                id, word, count = line.split()
                self.__update_dict(word, int(id), int(count))

    def size(self):
        self.__check()
        return len(self.word2id)

    def create_reseted_copy(self, corpus_name):
        self.__check()
        dict = copy.deepcopy(self)
        dict.filename = corpus_name
        dict.__word_count = 0
        for word in dict.word2count.keys():
            dict.word2count[word] = 0
        for id in dict.id2count.keys():
            dict.id2count[id] = 0
        w2c = defaultdict(int)
        with open_gz(dict.filename, encoding='utf-8') as file:
            for line in file:
                for word in line.lower().split():
                    w2c[word] += 1
        for word, count in w2c.items():
            if word in dict:
                id = dict.word2id[word]
                dict.word2count[word] = count
                dict.id2count[id] = count
                dict.__word_count += count
        return dict

    def create_dict(self):
        w2c = defaultdict(int)
        with open_gz(self.filename, encoding='utf-8') as file:
            for line in file:
                for word in line.lower().split():
                    w2c[word] += 1
        self.__reset()
        for word in list(w2c.keys()):
            if w2c[word] < self.min_occurrence:
                del w2c[word]
        for (word, count), id in zip(w2c.items(), itertools.count(start=0, step=1)):
            self.__update_dict(word, id, count)

    def load(self):
        if self.computed:
            self.load_computed()
        else:
            self.create_dict()

    def get_id(self, word):
        self.__check()
        return self.word2id[word]

    def get_word2count(self, word):
        self.__check()
        return self.word2count[word]

    def get_id2count(self, id):
        self.__check()
        return self.id2count[id]

    def get_word(self, id):
        self.__check()
        return self.id2word[id]

    @property
    def word_count(self):
        self.__check()
        return self.__word_count

    def __check(self):
        if not self.loaded:
            self.load()
        self.loaded = True

    def __contains__(self, item):
        self.__check()
        return item in self.word2count

    @staticmethod
    def is_entity(word):
        return word.lower().startswith('@!ent!')

    def filter(self, min_occurrences, keep_entities=False):
        self.__check()
        self.id2count.clear()
        self.id2word.clear()
        self.word2id.clear()
        word2count = self.word2count
        self.__word_count = 0
        self.word2count = {}
        id = 0
        for word, count in word2count.items():
            if count >= min_occurrences or (keep_entities and Dictionary.is_entity(word)):
                self.__update_dict(word, id, count)
                id += 1

    def get_count_for_minimum_occurrences(self, min_occurrences):
        self.__check()
        i = 0
        for word, count in self.word2count.items():
            if count >= min_occurrences:
                i += 1
        return i

    def get_missing_entity_count(self, min_occurrences):
        self.__check()
        i = 0
        for word, count in self.word2count.items():
            if count >= min_occurrences and Dictionary.is_entity(word):
                i += 1
        return i

    def random_words(self, count=1, exclude=set()):
        self.__check()
        aa = set(self.word2id.keys()) - exclude
        aa = list(aa)
        words = set()
        for i in range(count):
            words.add(choice(aa))
        return words

    def __add__(self, other):
        if not isinstance(other, Dictionary):
            raise Exception("Only dictionary type supported")
        self.__check()
        other.__check()
        self.__word_count += other.__word_count
        for word in self.word2count.keys():
            self.word2count[word] += other.word2count[word]
        for id in self.id2count.keys():
            self.id2count[id] = other.id2count[id]
        return self


class TaggerDictionary:
    tag2id = {}
    count = 0
    tag2count = {}

    def create_dict(self, filename):
        regex = re.compile(r'___| ')
        bfr = FileReader(filename)
        id = 0
        for block in bfr:
            items = regex.split(block.lower())
            for word, tag in list(zip(*2 * [iter(items)])):
                tag = tag.strip()
                try:
                    self.tag2count[tag] += 1
                except KeyError:
                    self.tag2count[tag] = 1
                    self.tag2id[tag] = id
                    id += 1

    def save(self, filename):
        if not filename.endswith('.dict'):
            filename += '.dict'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write("#dictionary version=%d size=%d\n" % (1, len(self.tag2id)))
            file.write("#id word count\n")
            for tag in self.tag2id.keys():
                file.write("%s %s %s\n" % (self.tag2id[tag], tag, self.tag2count[tag]))

    def load(self, filename):
        with open(filename, encoding='utf-8') as file:
            for line in file:
                if line.startswith("#"):
                    continue
                id, tag, count = line.split()
                count = int(count)
                id = int(id)
                self.tag2id[tag] = id
                self.tag2count[tag] = count
                self.count += count

    def filter(self, min_occurrences):
        self.tag2id = {}
        tag2count = self.tag2count
        id = 0
        for tag, count in tag2count.items():
            if count >= min_occurrences:
                self.tag2count[tag] = count
                self.tag2id[tag] = id
                id += 1

    def get_count_for_minimum_occurrences(self, min_occurrences):
        i = 0
        for word, count in self.tag2count.items():
            if count >= min_occurrences:
                i += 1
        return i

    def __contains__(self, item):
        return item in self.tag2count

    def get_id(self, word):
        return self.tag2id[word]