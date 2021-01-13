import numpy as np


def febs(a, b, c, r):
    # a diag, b upper diag, c sub diag,  r right hand side
    # Elimination: asume a neq 0 f.a. i
    dim = a.shape[0]
    for i in range(1, dim):
        gausratio = -c[i-1] / a[i-1]
        a[i] = a[i] + gausratio * b[i-1]
        r[i] = r[i] + gausratio * r[i-1]
    x = np.zeros(dim)
    x[-1] = r[-1] / a[-1]
    # substituation
    for i in range(1, dim):
        j = dim-i-1
        x[j] = (r[j] - b[j] * x[j+1]) / a[j]

    return x

'''
N = 4
a = 2*np.ones(N)
b = -1 * np.ones(N-1)
c = -1 * np.ones(N-1)
v = np.ones(N)  # /N ** 2
x = febs(a, b, c, v)
print("x=", x)
'''
