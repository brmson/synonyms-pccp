class Classes:
    def __init__(self, file):
        self.words = {}
        current_class = 0
        with open(file) as f:
            for line in f:
                if line == '\n':
                    current_class += 1
                else:
                    word = line.strip()
                    self.words[word] = current_class

    def get_class(self, word):
        return self[word]

    def __contains__(self, item):
        return item in self.words

    def __getitem__(self, item):
        return self.words[item]