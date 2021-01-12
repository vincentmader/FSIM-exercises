import numpy as np


def mult(a, b, c, v):
    # a = main diag, b upper diag, c sub, v vektor to multiply with

    c = np.append([0], c)
    b = np.append(b, [0])
    # alternative:
    return v*a + np.roll(v, -1)*b + np.roll(v, 1)*c


'''
    n = len(a)
    out = np.zeros(shape=(n, n))

    # first row of matrix
    out[0][0] = a[0] * v[0]
    out[0][1] = b[0] * v[1]

    # second to second-last rows
    for i in range(1, n-1):
        for j in range(1, n-1):
            if i == j:
                out[i][j] = a[i] * v[i]
            elif i == j-1:
                out[i][j] = b[i] * v[j] # b und c sollten hier vertauscht sein
            elif i == j+1:
                out[i][j] = c[i] * v[j]

    # last row
    out[-1][-2] = c[-2] * v[-2]
    out[-1][-1] = a[-1] * v[-1]

    return out
'''
'''
N = 4
a = np.array([2]*N)
b = - 1 * np.array([1., 2., 3.])
c = np.array([1, 2, 3])
v = np.arange(0, N)
x = mult(a, b, c, v)
print(x)
'''
