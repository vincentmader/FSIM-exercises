import numpy as np

from multigrid_matrices import *
from create_Diffmatrix import create_matrices
from v_cycle import main as v_cycle

D = 0.5
T0 = 1
L = 1
N = 65
e = 1

a, b, c, v = create_matrices(N, L*L*e/D, T0)
M = np.diag(a) + np.diag(b, 1) + np.diag(c, -1)

# c
R = restriction(int(N))
P = prolongation(int((N-1)/2+1))
print(M)
print(P@R@M)

# d
x = np.zeros(N)
<<<<<<< HEAD
x = Vcycle(M, v, x, 5, N, smooth=3, solve=40)
=======
x = v_cycle(M, v, x, 2, N, smooth=3, solve=40)
>>>>>>> 2dcc3bcbceaadfb5203dc1a80e3c5eac640254b2
print(x)


print("Done")
