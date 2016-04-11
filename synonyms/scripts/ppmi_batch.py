#!/usr/bin/env python3

__author__ = 'veselt12'
import argparse
from synonyms.in_out.utils import check_input_file_exists, save_mat, load_mat
from synonyms.ppmi import create_counts, transform, CONTEXT_TYPE
from synonyms.dictionary import Dictionary
import re
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Computes counts and ppmi matrix for given corpus and dictionary")
    parser.add_argument('matrices', type=str, nargs='+', help='Matrices')
    args = parser.parse_args()
    dictionaries = []
    matrices = args.matrices
    for matrix in args.matrices:
        dictionary = matrix.replace('.counts.mat', '.dict')
        check_input_file_exists(matrix)
        check_input_file_exists(dictionary)
        dictionaries.append(dictionary)

    for matrix, dictionary in zip(matrices, dictionaries):
        print('Processing:' + matrix)
        new_filename = matrix.replace('.counts.mat', '.ppmi')
        mat = load_mat(matrix)
        dict = Dictionary(dictionary)
        ppmi_matrix = transform(mat, dict)
        save_mat(ppmi_matrix, new_filename)
