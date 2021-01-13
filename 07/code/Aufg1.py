import numpy as np
import matplotlib.pyplot as plt
from febs import febs
from tridiag_matrix_mult import mult
from Jacobi import Jacobi_step
from create_Diffmatrix import create_matrices

D = 0.5
T0 = 1
L = 1
N = 8
e = 1

# 1f
N = 100
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_sp = febs(np.copy(a), np.copy(b), np.copy(c), np.copy(v))
x = np.linspace(-L, L, num=N)
plt.plot(x, T_sp, label="N=100")
plt.title("Temperture of radioaktive block")
plt.xlabel("Location")
plt.ylabel("Temperature")
plt.legend()
plt.savefig("../figures/Aufg1f.pdf")

# g
Res = mult(a, b, c, T_sp) - v
print(Res)

# i
N = 1000
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_sp = febs(np.copy(a), np.copy(b), np.copy(c), np.copy(v))
x_1000 = np.linspace(-L, L, num=N)
plt.plot(x_1000, T_sp, label="N=1000")
plt.title("Temperture of radioaktive block with febs")
plt.xlabel("Location")
plt.ylabel("Temperature")
plt.legend()
plt.savefig("../figures/Aufg1h.pdf")


# j and k
N = 8
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_ja = np.ones(N)
n = 32
x = np.linspace(-L, L, num=N)
plt.figure()
for i in range(n):
    T_ja = Jacobi_step(a, b, c, v, T_ja)
    plt.plot(x, T_ja)

plt.plot(x_1000, T_sp, label="true sol")
plt.title("Temperture of radioaktive block with Jacobi")
plt.xlabel("Location")
plt.ylabel("Temperature")
plt.legend()
plt.savefig("../figures/Aufg1k.pdf")

# k
N = 100
a, b, c, v = create_matrices(N, L*L*e/D, T0)
T_ja = np.ones(N)
n = 32
x = np.linspace(-L, L, num=N)
plt.figure()
for i in range(n):
    T_ja = Jacobi_step(a, b, c, v, T_ja)
    plt.plot(x, T_ja)

plt.plot(x_1000, T_sp, label="true sol")
plt.title("Temperture of radioaktive block with Jacobi")
plt.xlabel("Location")
plt.ylabel("Temperature")
plt.legend()
plt.savefig("../figures/Aufg1l.pdf")

print("Done.")
