import numpy as np
from multigrid_martices import *

def Jacobi(M, b, x, n):
    D = np.diag(M)
    LU = M - np.diag(D)
    for i in range(n):
        x = (b + LU@x)/D
    return x


def Vcycle(A, b, x, coarser, N, smooth=1, solve=10):
    # coarser = #times restrict and prologate
    x = np.zeros_like(b)
    Nresolution = []
    for i in range(len(coarser) + 1):
        Nresolution.append([(N-1)/2 + 1])
    # calculate residuals
    x = Jacobi(A, b, x, smooth)
    res = A@x - b
    R = restrict(Nresolution[0])
    P = prolongation(Nresolution[1])
    A = R @ A @ P
    rhs = R @ res
    if coarser == 0:
        err = Jacobi(A, b, err, solve)
    else:
        err = Vcycle(np.copy(A), x, res, coarser-1, Nresolution[1])
    x = x + P@err
    # 'solve' Problem
    eps =
        for i in range(coarser):

    return x
