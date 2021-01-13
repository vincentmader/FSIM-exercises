import numpy as np
from multigrid_martices import *
from create_Diffmatrix import create_matrices


def Jacobi(M, b, x, n):
    D = np.diag(M)
    LU = M - np.diag(D)
    for i in range(n):
        x = (b + LU@x)/D
    return x



D = 0.5
T0 = 1
L = 1
N = 9
e = 1
a, b, c, v = create_matrices(N, L*L*e/D, T0)

M = np.diag(a) + np.diag(b, 1) + np.diag(c, -1)

R = restriction(9)
P = prolongation(5)
print(M)
print(P@R@M)

print("Done")
