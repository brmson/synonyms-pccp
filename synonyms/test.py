__author__ = 'veselt12'
from .dictionary import Dictionary
from . import ppmi
from .in_out.utils import *
from time import time

dictionary = Dictionary("../test.dict", 50)
#dictionary.save('../test.dict')

matrix = ppmi.create_counts('../data.txt', '../test.dict', 1, ppmi.CONTEXT_TYPE.LR)
save_mat(matrix, 'counts.1.LR')
start = time()
matrix = ppmi.transform(matrix, dictionary)
save_mat(matrix, 'ppmi.1.LR')
print(time()-start)
