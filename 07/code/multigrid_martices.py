import numpy as np


def restriction(d):
    harray = np.diag([2] * d) + np.diag([1]*(d-1), 1) + np.diag([1]*(d-1), -1)
    return 1/4*harray[::2]


# print(restriction(3))


def prolongation(d):
    harray = np.zeros(((d-1)*2+1, d))
    harray[::2] = np.eye(d)
    y = np.array([1, 1] + [0]*(d-2))
    harray[1::2] = 0.5 * np.array([np.roll(y, i) for i in range(d-1)])
    return harray


# print(prolongation(2))
