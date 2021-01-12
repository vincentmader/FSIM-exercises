import numpy as np
from febs import febs
from tridiag_matrix_mult import mult


D = 0.5
N = 4
a = np.array([2.0]*N)
b = np.array([-1.0]*(N-1))
c = np.array([-1.0]*(N-1))
v = np.ones(N)/N ** 2
x = febs(np.copy(a), np.copy(b), np.copy(c), np.copy(v))
print("x=", x)
Res = mult(a, b, c, x) - v
print(Res)
