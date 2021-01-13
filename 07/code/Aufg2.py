import numpy as np
import matplotlib.pyplot as plt

from multigrid_matrices import *
from create_Diffmatrix import create_matrices
from v_cycle import main as v_cycle
from Jacobi import Jacobi_step
from tridiag_matrix_mult import mult
from febs import febs



D = 0.5
T0 = 1
L = 1
N = 9
e = 1

a, b, c, v = create_matrices(N, L*L*e/D, T0)
M = np.diag(a) + np.diag(b, 1) + np.diag(c, -1)

'''
# c
R = restriction(int(N))
P = prolongation(int((N-1)/2+1))
print(M)
print(P@R@M)
'''

# d
T_v = np.zeros(N)
T_v = v_cycle(M, v, T_v, 2, N, smooth=1, solve=1)
print(T_v)

# e

# a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_sp = febs(np.copy(a), np.copy(b), np.copy(c), np.copy(v))
n = 3
T_ja = np.zeros(N)
for i in range(n):
    T_ja = Jacobi_step(a, b, c, v, T_ja)

x = np.linspace(-L, L, num=N)
plt.plot(x, T_v, label="v-circle")
plt.plot(x, T_sp, label="exact diag")
plt.plot(x, T_ja, label="Jacobi")
plt.title("Temperature of radioactive block")
plt.xlabel("Location $x$")
plt.ylabel("Temperature $T$")
plt.legend()
plt.savefig("../figures/Aufg2e.pdf")

print("Done")
