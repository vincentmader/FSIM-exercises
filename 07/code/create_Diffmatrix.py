import numpy as np
def create_matrices(N, constant, T0):
    a = np.array([1.] + [-2.]*(N-2) + [1.])
    b = np.array([0] + [1.]*(N-2))
    c = np.array([1.]*(N-2) + [0])
    v = np.array([T0] + [-4.0*constant/(N*N)]*(N-2) + [T0])
    return a, b, c, v
