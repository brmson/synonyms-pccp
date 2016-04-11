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
    parser.add_argument('output_file', type=str, help='Name of the output file')
    parser.add_argument('matrices', type=str, nargs='+', help='Corpus in plain format')
    args = parser.parse_args()
    dictionaries = []
    matrices = args.matrices
    for matrix in args.matrices:
        dictionary = matrix.replace('.counts.mat', '.dict')
        check_input_file_exists(matrix)
        check_input_file_exists(dictionary)
        dictionaries.append(dictionary)

    mat = None
    dict = None
    for matrix, dictionary in zip(matrices, dictionaries):
        if mat is None:
            mat = load_mat(matrix)
            #print(mat.shape)
            dict = Dictionary(dictionary)
        else:
            a = load_mat(matrix)
            #print(matrix, a.shape)
            mat = mat + a
            dict = dict + Dictionary(dictionary)
    save_mat(mat, args.output_file+'.counts')
    dict.save(args.output_file+'.dict')