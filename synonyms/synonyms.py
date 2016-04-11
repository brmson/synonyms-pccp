from scipy.sparse import lil_matrix
from sklearn.preprocessing import normalize
import numpy as np
from tempfile import TemporaryFile


class SVDModel:
    def __init__(self, matrix_U, matrix_S, dictionary, caron_p=0.25, dimensions=1000):
        self.U = matrix_U
        self.s = lil_matrix((matrix_S.shape[1], matrix_S.shape[1]))
        self.s.setdiag(matrix_S[0])
        self.s = self.s.tocsr()
        self.dictionary = dictionary
        self._caron_p = caron_p
        self._dimensions = dimensions
        self._computed = False

    def __update_matrix(self):
        if self.dimensions > self.U.shape[0]:
            raise ValueError('number of requested dimensions is bigger than number of dimension in matrix')
        size = self.s.shape[1]
        dimensions = self.dimensions
        s = self.s[size - dimensions:, size - dimensions:].copy()
        s.data **= self.caron_p
        u = self.U[:, size - dimensions:]
        matrix = u * s
        matrix = normalize(matrix, norm="l2", axis=1)
        self.matrix = np.matrix(matrix)
        self._computed = True

    def get_synonyms(self, target_word, k, return_ids=True, return_score=False):
        if not self._computed:
            self.__update_matrix()
        target_id = self.dictionary.get_id(target_word)
        score = list(map(abs, np.asarray(self.matrix[target_id, :] * self.matrix.T)[0, :]))
        sorted_ids = np.argsort(score, axis=None)[::-1]
        data = (list(map(lambda x: self.dictionary.get_word(x), sorted_ids[1:k + 1])), )
        if return_ids:
            data += (sorted_ids[1:k + 1], )
        if return_score:
            data += ([score[id] for id in sorted_ids[1:k + 1]], )
        return data

    @property
    def caron_p(self):
        return self._caron_p

    @caron_p.setter
    def caron_p(self, caron_p):
        self._caron_p = caron_p
        self._computed = False

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        self._dimensions = dimensions
        self._computed = False


class SVDToOneModel(SVDModel):
    def __init__(self, matrix_U, matrix_S, dictionary, caron_p=0.25, dimensions=1000, to_one=100):
        self._to_one = to_one
        self.diag = matrix_S[0]
        super(SVDToOneModel, self).__init__(matrix_U, matrix_S, dictionary, caron_p, dimensions)

    def __update_matrix(self):
        if self.dimensions > self.U.shape[0]:
            raise ValueError('number of requested dimensions is bigger than number of dimension in matrix')
        size = len(self.diag)
        dimensions = self.dimensions
        s = self.s[size - dimensions:, size - dimensions:].copy()
        diag = self.diag.copy()
        diag[-self.to_one:] = 1
        s = s.setdiag(diag)
        print(s)
        u = self.U[:, size - dimensions:]
        matrix = u * s
        matrix = normalize(matrix, norm="l2", axis=1)
        self.matrix = np.matrix(matrix)
        self._computed = True

    @property
    def to_one(self):
        return self._to_one

    @to_one.setter
    def to_one(self, to_one):
        self._to_one = to_one
        self._computed = False

#
# class SVDModelMemMap(SVDModel):
#     def __init__(self, matrix_U, matrix_S, dictionary, caron_p=0.25, dimensions=10000):
#         self.U = matrix_U
#         self.s = lil_matrix((matrix_S.shape[1], matrix_S.shape[1]))
#         self.s.setdiag(matrix_S[0])
#         self.s = self.s.tocsr()
#         self.dictionary = dictionary
#         self._caron_p = caron_p
#         self._dimensions = dimensions
#         self._computed = False
#         self.matrix = None
#         self.__update_matrix()
#
#     def __update_matrix(self):
#         if self.dimensions > self.U.shape[0]:
#             raise ValueError('number of requested dimensions is bigger than number of dimension in matrix')
#         size = self.s.shape[1]
#         dimensions = self.dimensions
#         s = self.s[size - dimensions:, size - dimensions:].copy()
#         s.data **= self.caron_p
#         print('creating new matrix')
#         self.matrix = np.memmap(TemporaryFile(), dtype='float32', mode='w+', shape=(self.U.shape[0], dimensions))
#         self.matrix[:] = self.U[:, size - dimensions:]
#         # self.matrix[:] *= s
#         print('normalizing')
#         self.normalize(self.matrix)
#         print('normalized')
#         self._computed = True
#
#     @staticmethod
#     def normalize(matrix):
#         for row in range(matrix.shape[0]):
#             matrix[row, :] /= np.sqrt(np.sum(matrix[row, :] ** 2))
#
#     def get_synonyms(self, target_word, k, return_ids=True, return_score=False):
#         if not self._computed:
#             self.__update_matrix()
#         target_id = self.dictionary.get_id(target_word)
#         score = list(map(abs, np.asarray(self.matrix[target_id, :] * self.matrix.T)[0, :]))
#         sorted_ids = np.argsort(score, axis=None)[::-1]
#         data = (list(map(lambda x: self.dictionary.get_word(x), sorted_ids[1:k + 1])), )
#         if return_ids:
#             data += (sorted_ids[1:k + 1], )
#         if return_score:
#             data += ([score[id] for id in sorted_ids[1:k + 1]], )
#         return data