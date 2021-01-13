import numpy as np
from multigrid_martices import *
from create_Diffmatrix import create_matrices
from v_cicle import Vcycle

D = 0.5
T0 = 1
L = 1
N = 9
e = 1

a, b, c, v = create_matrices(N, L*L*e/D, T0)
M = np.diag(a) + np.diag(b, 1) + np.diag(c, -1)

x = np.zeros(N)
x = Vcycle(M, v, x, 2, N,smooth=3, solve=40)
print(x)

# P = prolongation(N)
# R = restriction(N)
# print(M)
# print(P@R@M)

print("Done")
