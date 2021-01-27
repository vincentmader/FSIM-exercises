import numpy as np
import matplotlib.pyplot as plt


def advect(qold, vold, dx, dt):
    masksym = np.where(vold[:-1]*vold[1:] < 0)
    maskupwind = list(
            set(np.where(np.sign(v[1:]) == 1)[0]) &
            set(np.where(np.sign(v[:-1]) == 1)[0])
            )
    maskdownwind = list(
        set(np.where(np.sign(v[1:]) == -1)[0]) &
        set(np.where(np.sign(v[:-1]) == -1)[0])
                     )
    # print(masksym)
    # print(maskupwind)
    # print(maskdownwind)
    v_mean = (vold[1:] + vold[:-1])/2
    # symmetric
    qold[1:-1][masksym] -= (qold[2:][masksym] - qold[:-2][masksym]) / (2*dx) * \
                                v_mean[masksym] * dt
    # upwind
    qold[1:-1][maskupwind] -= (qold[1:-1][maskupwind] - qold[:-2][maskupwind])\
                                / dx * vold[:-1][maskupwind] * dt
    # downwind
    qold[1:-1][maskdownwind] -= (qold[2:][maskdownwind] - qold[1:-1][maskdownwind]) / dx \
                                * vold[1:][maskdownwind] * dt
    return qold


x_N = 100
L = 10
dx = L/x_N
v = np.ones(x_N+1)
x = np.linspace(-L/2-dx, L/2+dx, num=x_N+2)
q_0 = (x - np.abs(x))/(2*x)
dt = 3.0 / 100
for i in range(x_N):
    q_0 = advect(q_0, v, dx, dt)
plt.plot(x, q_0)
plt.savefig("../figures/plot1.png")


v = -2/L * np.linspace(-L/2-dx/2, L/2 + dx/2, x_N+1)
# print(x)
# print(v)
q_0 = np.zeros_like(x)
for i in range(len(x)):
    # print(np.abs(x[i]), L/4)
    if (np.abs(x[i]) < L/4):
        q_0[i] = 1
# print(len(q_0))
plt.figure()
plt.plot(x, q_0, label="0")
for i in range(x_N):
    q_0 = advect(q_0, v, dx, dt)
plt.plot(x, q_0, label="1")
plt.legend()
plt.savefig("../figures/plot2.png")

print('Done.')
