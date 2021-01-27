import numpy as np
import matplotlib.pyplot as plt


def advection(q_0, scheme="upwind", v=1, xN=100, L=10, t_end=3, tN=100, bc=[1, 0]):
    dx = xN / L
    dt = t_end / tN

    # reserve storange
    q_all = np.zeros((tN+1, xN+2))

    # initial condition
    q_all[0, :] = q_0

    # boundary condition
    q_all[:, 0] = bc[0] * np.ones(tN+1)
    q_all[:, -1] = bc[1] * np.ones(tN+1)

    # symmetric
    for i in range(tN):
        if scheme == "symmetric":
            q_x = (q_all[i, 2:] - q_all[i, :-2]) / (2*dx)
        if scheme == "upwind":
            q_x = (q_all[i, 1:-1] - q_all[i, :-2]) / dx
        if scheme == "downwind":
            q_x = (q_all[i, 2:] - q_all[i, 1:-1]) / dx

        # taylorstep
        q_all[i+1, 1:-1] = q_all[i, 1:-1] - 1*v*q_x*dt
    return q_all


v = 1
xN = 100
L = 10
t_end = 3
tN = 100
dx = xN/L
dt = t_end / tN

x = np.linspace(-L/2-dx, L/2+dx, num=xN+2)
q_0 = (x - np.abs(x))/(2*x)
q_sym = advection(q_0, t_end=30, tN=1000, bc=[0.5, 0])
plt.plot(x, q_sym[0], label="0")
plt.plot(x, q_sym[10], label="10")
plt.plot(x, q_sym[20], label="20")
plt.plot(x, q_sym[1000], label="100")
plt.legend()
plt.savefig("test.png")
# plt.show()

print("Done.")
