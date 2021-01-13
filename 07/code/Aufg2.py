import numpy as np

from multigrid_matrices import prolongation, restriction
from create_Diffmatrix import create_matrices
from v_cycle import main as v_cycle

D = 0.5
T0 = 1
L = 1
N = 65
e = 1

a, b, c, v = create_matrices(N, L*L*e/D, T0)
M = np.diag(a) + np.diag(b, 1) + np.diag(c, -1)

# 1. c)
R = restriction(int(N))
P = prolongation(int((N-1)/2+1))
print(M)
print(P@R@M)

# 1. d)
x = np.zeros(N)
x = v_cycle(M, v, x, 2, N, smooth=3, solve=40)
print(x)


print("Done")
