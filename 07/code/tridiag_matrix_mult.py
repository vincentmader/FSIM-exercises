import numpy as np


def mult(a, b, c, v):
    # a = main diag, b upper diag, c sub, v vektor to multiply with
    c = np.append([0], c)
    b = np.append(b, [0])
    return v*a + np.roll(v, -1)*b + np.roll(v, 1)*c


N = 4
a = np.array([2]*N)
b = - 1 * np.array([1., 2., 3.])
c = np.array([1, 2, 3])
v = np.arange(0, N)
x = mult(a, b, c, v)
print(x)
