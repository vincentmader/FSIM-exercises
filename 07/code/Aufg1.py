import matplotlib.pyplot as plt
import numpy as np

from febs import febs

from Jacobi import Jacobi_step
from tridiag_matrix_mult import mult
from create_Diffmatrix import create_matrices


D = 0.5
T0 = 1
L = 1
N = 8
e = 1

# 1. f)
N = 100
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_sp = febs(np.copy(a), np.copy(b), np.copy(c), np.copy(v))
x = np.linspace(-L, L, num=N)
plt.plot(x, T_sp, label="N=100")
plt.title("Temperature of radioactive block")
plt.xlabel("Location $x$")
plt.ylabel("Temperature $T$")
plt.legend()
plt.savefig("../figures/Aufg1f.pdf")

# 1. g)
Res = mult(a, b, c, T_sp) - v
print(Res)

# 1. i)
N = 1000
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_sp = febs(np.copy(a), np.copy(b), np.copy(c), np.copy(v))
x_1000 = np.linspace(-L, L, num=N)
plt.plot(x_1000, T_sp, label="N=1000")
plt.title("Temperature of radioactive block with febs")
plt.xlabel("Location $x$")
plt.ylabel("Temperature $T$")
plt.legend()
plt.savefig("../figures/Aufg1h.pdf")


# 1. j) & k)
N = 8
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_ja = np.ones(N)

n = 30
x = np.linspace(-L, L, num=N)
plt.figure()  # needed later

for i in range(n):
    T_ja = Jacobi_step(a, b, c, v, T_ja)
    plt.plot(x, T_ja)

plt.plot(x_1000, T_sp, label="true solution")
plt.title("Temperature of radioactive block with Jacobi")
plt.xlabel("Location $x$")
plt.ylabel("Temperature $T$")
plt.legend()
plt.savefig("../figures/Aufg1k.pdf")

# 1. k)
N = 100
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_ja = np.ones(N)

n = 30
x = np.linspace(-L, L, num=N)
plt.figure()  # needed later

for i in range(n):
    T_ja = Jacobi_step(a, b, c, v, T_ja)
    plt.plot(x, T_ja)

plt.plot(x_1000, T_sp, label="true solution")
plt.title("Temperature of radioactive block with Jacobi")
plt.xlabel("Location $x$")
plt.ylabel("Temperature $T$")
plt.legend()
plt.savefig("../figures/Aufg1l.pdf")


print("Done.")
