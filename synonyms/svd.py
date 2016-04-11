#!/usr/bin/env python3
import sys
import numpy as np
#from sparsesvd import sparsesvd
from scipy.io import *
from scipy.sparse import *
from scipy.sparse.linalg import svds
def svd(input_file,output_file,factors):
    mat=loadmat(input_file)["mat"]
    if not isspmatrix_csc(mat):
        mat=mat.tocsc()
    #U,s,V=sparsesvd(mat, factors)
    #s**=caronP
    #x=U.T*s

    U,s,V=svds(mat, factors)
#    savemat(output_file,{'U':U,'s':s},oned_as='row')
    np.savez(output_file,U=np.matrix(U),s=np.matrix(s))
#    s**=caronP
#    x=U*s

#    mat=np.matrix(x)
#    np.save(output_file, mat)


if __name__=='__main__':
    if len(sys.argv)<4:
        print ("missing arguments")
        print ("input_file output_file factors")
        exit(1)
    svd(sys.argv[1],sys.argv[2],int(sys.argv[3]))
