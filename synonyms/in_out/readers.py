import subprocess
from multiprocessing.queues import Empty

__author__ = 'veselt12'

from multiprocessing import Process, JoinableQueue, Event
import gzip, io


class FileReader(Process):
    def __init__(self, filename, buffer_size=1000):
        super(FileReader, self).__init__()
        self.filename = filename
        self.que = JoinableQueue(buffer_size)
        self.event = Event()
        self.event.set()
        self.started = Event()
        self.started.clear()

    # It's crucial to call task_done on the queue after the item was processed
    def get_queue(self):
        return self.que

    def get_event(self):
        return self.event

    def is_done(self):
        return not self.event.is_set() and self.que.empty()

    def run(self):
        self.started.set()
        self.proc()
        self.event.clear()

    def proc(self):
        with open_gz(self.filename, encoding='utf-8') as file:
            for line in file:
                self.que.put(line)

    def __iter__(self):
        self.start()
        self.started.wait()
        while not self.is_done():
            try:
                text = self.que.get(timeout=0.1)
                yield text
                self.que.task_done()
            except Empty:
                pass


class BlockFileReader(FileReader):
    def proc(self):
        with open_gz(self.filename, encoding='utf-8') as file:
            buffer = []
            for line in file:
                if line == '\n':
                    self.que.put("".join(buffer))
                    buffer = []
                else:
                    buffer.append(line)


def open_gz(file, mode='r', encoding='utf-8'):
    if file.endswith('.gz'):
        return io.TextIOWrapper(gzip.open(file, mode=mode), encoding=encoding)
    return open(file, mode=mode, encoding=encoding)