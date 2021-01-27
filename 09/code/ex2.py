import numpy as np


def advect(qold, vold, dx, dt):
    masksym = [vold[:-1]*vold[1:] < 0]
    maskupwind = np.logical_and(np.logical_not(masksym), vold[:-1] > 0)
    maskdownwind = np.logical_and(np.logical_not(masksym), vold[:-1] <= 0)
    q_x = np.zeros_like(qold)
    v_mean = (vold[1:] + vold[:-1])/2
    # symmetric
    qold[1:-1][masksym] -= (qold[2:][masksym] - qold[:-2][masksym]) / (2*dx) * \
                                v_mean[masksym] * dt
    # upwind
    qold[1:-1][maskupwind] -= (qold[1:-1][maskupwind] - qold[:-2][maskupwind])\
                                / dx * vold[:-1] * dt
    # downwind
    qold[1:-1][maskdownwind] -= (qold[2:][maskdownwind] - qold[1:-1][maskdownwind]) / dx \
                                *vold[1:] * dt
    return qold



print('Done.')
