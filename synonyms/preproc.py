import re
import unicodedata
import nltk
from nltk.tokenize import RegexpTokenizer

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
with open('../Gastro.txt') as f, open('../Gastro_preproc.txt', 'w') as ff:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue
        words = tokenizer.tokenize(line)
        w_out = []
        for word in words:
            w = strip_accents(word.strip())
            w = re.sub('[^A-Za-z0-9\.]+', '', w)
            if len(w) < 2:
                continue
            if w.isalpha():
                w_out.append(w)
            elif w.isdigit():
                w_out.append("!NUMBER_TOKEN!")
            elif w[:-1].isalpha():
                w_out.append(w[:-1])
            elif w.isalnum():
                w_out.append("!NUMBER_ALPHA_TOKEN!")
            else:
                w_out.append("!OTHER_TOKEN!")
        if len(w_out) > 0:
            ff.write(" ".join(w_out))
            ff.write("\n")
