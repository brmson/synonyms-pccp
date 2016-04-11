from collections import defaultdict
import json
from synonyms.in_out.readers import open_gz


class POS:
    def __init__(self):
        self.word_pos = {}

    def __getitem__(self, item):
        return self.word_pos[item]

    def save(self, filename):
        with open_gz(filename, 'w') as f:
            json.dump(self.word_pos, f)

    @staticmethod
    def load(filename):
        pos = POS()
        with open_gz(filename) as f:
            pos.word_pos = json.load(f)
        return pos

    @staticmethod
    def create(file):
        tags = defaultdict(lambda: defaultdict(int))
        with open_gz(file) as f:
            for line in f:
                if line != '\n' and len(line) >= 3:
                    word = line.strip()
                    if word[-2] == '_':
                        p = word[-1]
                        w = word[:-2]
                        tags[w][p] += 1
        pos = POS()
        for word, t in tags.items():
            max_num = 0
            for tag, num in t.items():
                if num > max_num:
                    pos.word_pos[word] = t
                    max_num = num
        return pos