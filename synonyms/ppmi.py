__author__ = 'veselt12'
from .in_out.readers import FileReader, BlockFileReader
import multiprocessing, math, itertools
from multiprocessing import Process, Queue
from multiprocessing.queues import Empty
from collections import defaultdict, deque
from scipy.sparse import coo_matrix
import re


class CONTEXT_TYPE:
    LR = 'LR'
    L = 'L'
    R = 'R'


class CountsWorker(Process):
    def __init__(self, que, out_queue, event, dictionary, context_size, context_type):
        super(CountsWorker, self).__init__()
        self.que = que
        self.out_queue = out_queue
        self.event = event
        self.dictionary = dictionary
        self.context_size = context_size
        self.context_type = context_type

    def __proc(self, words):
        context = deque(maxlen=self.context_size)
        for word in words:
            if word in self.dictionary:
                word_id = self.dictionary.get_id(word)
                for c in context:
                    if word_id not in self.data:
                        self.data[word_id] = {}
                    if c not in self.data[word_id]:
                        self.data[word_id][c] = 0
                    self.data[word_id][c] += 1
                context.append(word_id)

    def run(self):
        self.data = {}
        while self.event.is_set() or not self.que.empty():
            try:
                text = self.que.get(timeout=0.1)
                words = text.lower().split()
                if self.context_type == CONTEXT_TYPE.L:
                    self.__proc(words)
                elif self.context_type == CONTEXT_TYPE.R:
                    self.__proc(words[::-1])
                else:
                    self.__proc(words)
                    self.__proc(words[::-1])
                self.que.task_done()
            except Empty:
                pass
        self.out_queue.put(self.data)


def create_counts(file, dictionary, context_size, context_type):
    reader = FileReader(filename=file, buffer_size=1000)
    reader.start()
    que = reader.get_queue()
    event = reader.get_event()
    workers_count = 2  # multiprocessing.cpu_count()
    out_queue = Queue(maxsize=workers_count)
    workers = [CountsWorker(que, out_queue, event, dictionary, context_size, context_type) for _ in
               range(workers_count)]
    [worker.start() for worker in workers]
    rows = []
    cols = []
    vals = []
    for _ in range(workers_count):
        dict_matrix = out_queue.get()
        for row, data in dict_matrix.items():
            for col, value in data.items():
                rows.append(row)
                cols.append(col)
                vals.append(value)
    matrix = coo_matrix((vals, (rows, cols)), shape=(dictionary.size(), dictionary.size(),)).tocsr()
    [worker.join() for worker in workers]
    que.join()
    return matrix


def process(dict, tagger_dict, items, context_size, data):
    context = deque(maxlen=context_size)
    for word, tag in items:
        if word in dict and tag in tagger_dict:
            word_id = dict.get_id(word)
            tag_id = tagger_dict.get_id(tag)
            for c in context:
                if word_id not in data:
                    data[word_id] = {}
                if c not in data[word_id]:
                    data[word_id][c] = 0
                data[word_id][c] += 1
            context.append(tag_id)


def create_counts_tagger(file, dict, tagger_dict, context_size):
    bfr = BlockFileReader(file)
    regex = re.compile(r'___| ')
    data = {}
    for block in bfr:
        items = regex.split(block.lower())
        process(dict, tagger_dict, items, context_size, data)
        process(dict, tagger_dict, items[::-1], context_size, data)
    rows = []
    cols = []
    vals = []
    for row, d in data.items():
        for col, value in d.items():
            rows.append(row)
            cols.append(col)
            vals.append(value)
    matrix = coo_matrix((vals, (rows, cols)), shape=(dict.size(), tagger_dict.size(),)).tocsr()
    return matrix


def transform(matrix, dictionary):
    matrix = matrix.asfptype().tocoo()
    for row, col, val, i in zip(matrix.row, matrix.col, matrix.data, itertools.count(0, 1)):
        matrix.data[i] = max(0, math.log(
            val * dictionary.word_count / dictionary.get_id2count(row) / dictionary.get_id2count(col)))
    return matrix.tocsr()
