import numpy as np

def febs(a, b, c, r):
    # a diag, b upper diag, c sub diag,  r right hand side
    # Elimination: asume a neq 0 f.a. i
    dim = a.shape[0]
    # a_elem = np.append(a[0], np.zeros(dim-1))
    # r_elem = np.append(r[0], np.zeros(dim-1))

    for i in range(1, dim):
        print("\n", i)
        print(a[i-1])
        gausratio = -c[i-1] / a[i-1]
        # print(gausratio)
        # print(b[i-1], a[i], gausratio * b[i-1])
        a[i] = a[i] + gausratio * b[i-1]
        # print(r[i], r[i-1], gausratio * r[i-1])
        r[i] = r[i] + gausratio * r[i-1]
        # print(i, gausratio)
        # print(a, "\n")
        # print("\n")
    # print(a)
    # print(b)
    # print(r)
    # substitution
    x = np.zeros(dim)
    x[-1] = r[-1] / a[-1]
    for i in range(1, dim):
        # print(x)
        j = dim-i-1
        x[j] = (r[j] - b[j] * x[j+1]) / a[j]
        # print(x[j])
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
