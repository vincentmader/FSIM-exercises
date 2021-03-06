import numpy as np
from tridiag_matrix_mult import mult


def Jacobi_step(a, b, c, r, x):

    dim = a.shape[0]
    return r/a + mult(np.zeros(dim), -b, -c, x)/a
