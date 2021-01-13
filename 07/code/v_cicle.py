import numpy as np
from multigrid_martices import *

def Jacobi(M, b, x, n):
    D = np.diag(M)
    LU = np.diag(D)-M
    for i in range(n):
        x = (b + LU@x)/D
    return x


def Vcycle(A, b, x, coarser, N, smooth=1, solve=10):
    # coarser = #times restrict and prologate
    print(coarser)
    # x = np.zeros_like(b)
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
        # solve on coarstest grid
        err = Jacobi(A_2h, r_2h, err, solve)
    else:
        err = Vcycle(np.copy(A_2h), r_2h, err, coarser-1, Nnext)
    print(coarser)
    x = x + P@err
    x = Jacobi(A, b, x, smooth)
    return x
