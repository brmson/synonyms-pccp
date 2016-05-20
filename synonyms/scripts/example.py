#!/usr/bin/python3
# vim: set fileencoding=utf8
#
# Usage: synonyms/scripts/example.py DICT UMATRIX SMATRIX WORD
#
# Example: synonyms/scripts/example.py data_synonyms/nametag.1.LR.dict data_synonyms/nametag.1.LR.ppmi.mat.10000.svd.U.mtx.gz data_synonyms/nametag.1.LR.ppmi.mat.10000.svd.s.mtx.gz manžel

import sys
sys.path.append('.')

from synonyms.dictionary import Dictionary
from synonyms.synonyms import SVDModel
import numpy as np
from scipy.io import mmread


print(sys.argv[1])
dictionary = Dictionary(filename=sys.argv[1])
print(sys.argv[3])
s = mmread(sys.argv[3])
print(sys.argv[2])
U = mmread(sys.argv[2])
print('SVDModel')
model = SVDModel(U, s, dictionary)
model.dimensions = 2500
model.caron_p = 0.25
print('get_synonyms')
synonyms, ids, score = model.get_synonyms(sys.argv[4], 10, return_ids=True, return_score=True)
print(synonyms, ids, score)
