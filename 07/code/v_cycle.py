import numpy as np

from multigrid_matrices import *


def Jacobi(M, b, x, n):

    D = np.diag(M)
    LU = np.diag(D)-M

    for i in range(n):
        x = (b + LU@x)/D

    return x


def main(A, b, x, coarser, N, smooth=1, solve=10):
    # coarser = nr. of times to restrict and prolongate

    Nnext = (N-1)/2 + 1

    # calculate residuals
    x = Jacobi(A, b, x, smooth)
    res = b - A@x

    # transform to smaler gridzize
    R = restriction(int(N))
    P = prolongation(int(Nnext))
    A_2h = R @ A @ P
    r_2h = R @ res

    err = np.zeros_like(r_2h)
    if coarser == 1:  # pre coarstest grid
        # solve on coarse test grid
        err = Jacobi(A_2h, r_2h, err, solve)
    else:
        err = main(np.copy(A_2h), r_2h, err, coarser-1, Nnext)

    x = x + P@err
    x = Jacobi(A, b, x, smooth)

    return x
