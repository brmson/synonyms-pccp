import os.path
from scipy.io import savemat, loadmat
from scipy.sparse import isspmatrix
import numpy as np


def __save_sparse(matrix, filename):
    savemat(filename, {'mat': matrix}, oned_as='row')


def __save_dense(matrix, filename):
    np.save(filename, matrix)


def save_mat(matrix, filename):
    if isspmatrix(matrix):
        __save_sparse(matrix, filename)
    else:
        __save_dense(matrix, filename)


def __load_sparse(filename):
    return loadmat(filename)['mat']


def __load_dense(filename):
    return np.load(filename)


def load_mat(filename):
    if filename.endswith('.mat'):
        return __load_sparse(filename)
    return __load_dense(filename)


def check_input_file_exists(filename):
    if not os.path.isfile(filename):
        SystemExit("File \""+filename+"\" doesn't exists")