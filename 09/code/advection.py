import numpy as np


def main(
    q_0, scheme="upwind", v=1, x_N=100, L=10,
    t_end=3., t_N=100, boundary_conditions=[1, 0]
):
    dx = x_N / L
    dt = t_end / t_N
    # reserve storage
    q_all = np.zeros((t_N+1, x_N+2))
    # initial condition
    q_all[0, :] = q_0
    # boundary condition
    q_all[:, 0] = boundary_conditions[0]*np.ones(t_N+1)
    q_all[:, -1] = boundary_conditions[1]*np.ones(t_N+1)

    for i in range(t_N):
        if scheme == "symmetric":
            q_x = (q_all[i, 2:]-q_all[i, :-2])/(2*dx)
        if scheme == "upwind":
            q_x = (q_all[i, 1:-1]-q_all[i, :-2])/dx
        if scheme == "downwind":
            q_x = (q_all[i, 2:]-q_all[i, 1:-1])/dx
        # taylorstep
        q_all[i+1, 1:-1] = q_all[i, 1:-1]-1*v*q_x*dt

    return q_all
