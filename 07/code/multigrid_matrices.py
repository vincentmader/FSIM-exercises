import numpy as np


def restriction(d):

    helper_array = np.diag([2] * d)
    helper_array += np.diag([1]*(d-1), 1)
    helper_array += np.diag([1]*(d-1), -1)

    return 1/4 * helper_array[::2]


# print(restriction(3))


def prolongation(d):

    helper_array = np.zeros(((d-1)*2+1, d))
    helper_array[::2] = np.eye(d)

    helper_array2 = np.array([1, 1] + [0]*(d-2))
    helper_array[1::2] = 0.5 * np.array(
        [np.roll(helper_array2, i) for i in range(d-1)]
    )

    return helper_array


# print(prolongation(2))
