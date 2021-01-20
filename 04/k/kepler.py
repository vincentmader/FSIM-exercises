import numpy as np
import matplotlib.pyplot as plt
import time


### Numerics

def acc(x1, x2=np.array([0, 0, 0])):
    return 1 / np.sum((x1-x2)**2)**(3/2) * (x2-x1)


def leapfrog(q, dt):
    x = q[:3]
    v = q[3:]
    v_1_2 = v + acc(x) * dt / 2
    x_1 = x + dt * v_1_2
    v_1 = v_1_2 + acc(x_1) * dt / 2
    q1 = np.concatenate((x_1, v_1))
    return q1


def f(x):                                       # x[3:] are the velocities,
    return np.concatenate((x[3:], acc(x[:3])))  # x[:3] the positional coordina


def RK2(y, dt):
    k1 = dt * f(y)
    k2 = dt * f(y+k1)
    return y + 0.5 * (k1+k2)


def RK4(y, dt):
    k1 = dt * f(y)
    k2 = dt * f(y + 0.5*k1)
    k3 = dt * f(y + 0.5*k2)
    k4 = dt * f(y + k3)
    return y + (1/6) * (k1+2*k2+2*k3+k4)


### Conserved quanteties


def xModulus(x):
    return np.sqrt(np.sum(x[:, :3] ** 2, axis=1))


def pModulus(x):
    return np.sqrt(np.sum(x[:, 3:] ** 2, axis=1))


def energy(x):
    return 0.5 * pModulus(x) ** 2 - 1 / xModulus(x)


def angularMom(x):
    return np.array([x[:, 1] * x[:, 5] - x[:, 2] * x[:, 4],
                        x[:, 2] * x[:, 3] - x[:, 0] * x[:, 5],
                        x[:, 0] * x[:, 4] - x[:, 1] * x[:, 3]])


def runge_Lenz(x):
    aM = angularMom(x)
    harray1 = np.array([x[:, 4] * aM[2, :] - x[:, 5] * aM[1, :],
                        x[:, 5] * aM[0, :] - x[:, 3] * aM[2, :],
                        x[:, 3] * aM[1, :] - x[:, 4] * aM[0, :]])
    harray2 = np.array([xModulus(x), xModulus(x), xModulus(x)])
    return harray1 - (x[:, :3] / harray2.T).T


### Set values

n_orbit = 100                     # number of orbits
n_steps = 1000                    # number of steps per orbit
n = n_orbit*n_steps                 # total number of steps
dt = 2*np.pi/n_steps               # step-size
x_0 = np.array([1, 0, 0])             # initial position
v_0 = np.array([0, 0.5, 0])           # initial velocity
t = np.linspace(0, n_orbit, num=n)

x_lf = np.zeros((n, 6))                    # initializing 6-vector for leapfrog
x_lf[0, :] = np.concatenate((x_0, v_0))

x_rk2 = np.zeros((n, 6))                      # initializing 6-vector for RK2
x_rk2[0, :] = np.concatenate((x_0, v_0))

x_rk4 = np.zeros((n, 6))                      # initializing 6-vector for RK4
x_rk4[0, :] = np.concatenate((x_0, v_0))

t_lf = 0
t_rk2 = 0
t_rk4 = 0


### Calculating

for i in range(1, n):                        # iterating over all n steps
    t1 = time.time()
    x_lf[i] = leapfrog(x_lf[i-1], dt)
    t2 = time.time()
    x_rk2[i] = RK2(x_rk2[i-1], dt)
    t3 = time.time()
    x_rk4[i] = RK4(x_rk4[i-1], dt)
    t4 = time.time()
    t_lf += t2 - t1
    t_rk2 += t3 - t2
    t_rk4 += t4 - t3

print('leapfrog: ', t_lf)
print('rk2: ', t_rk2)
print('rk4: ', t_rk4)

xModulus_rk2 = xModulus(x_rk2)
pModulus_rk2 = pModulus(x_rk2)
energy_rk2 = 0.5 * pModulus_rk2 ** 2 - 1 / xModulus_rk2
angularMom_rk2 = angularMom(x_rk2)
rungeLenz_rk2 = runge_Lenz(x_rk2)


xModulus_rk4 = xModulus(x_rk4)
pModulus_rk4 = pModulus(x_rk4)
energy_rk4 = 0.5 * pModulus_rk4 ** 2 - 1 / xModulus_rk4
angularMom_rk4 = angularMom(x_rk4)
rungeLenz_rk4 = runge_Lenz(x_rk4)


xModulus_lf = xModulus(x_lf)
pModulus_lf = pModulus(x_lf)
energy_lf = 0.5 * pModulus_lf ** 2 - 1 / xModulus_lf
angularMom_lf = angularMom(x_lf)
rungeLenz_lf = runge_Lenz(x_lf)


### Plotting

plt.figure()
plt.plot(t, energy_rk2, label='RK2')
plt.plot(t, energy_rk4, label='RK4')
plt.plot(t, energy_lf, linewidth=0.1, label='LF')          # change for n > 100
plt.xlabel('Time [orbits]')
plt.ylabel('Energy []')
plt.legend()
plt.title('Evolution of energy')
plt.savefig('energy' + str(n_orbit) + '.png', fmt='png', dpi=200)
# plt.show()

plt.figure()
plt.plot(rungeLenz_rk2[0, :], rungeLenz_rk2[1, :], label='RK2')
plt.plot(rungeLenz_rk4[0, :], rungeLenz_rk4[1, :], label='RK4')
plt.plot(rungeLenz_lf[0, :], rungeLenz_lf[1, :], linewidth=0.1, label='LF')
plt.xlabel('x_Runge_Lenz')
plt.ylabel('y_Runge_Lenz')
plt.legend()
plt.title('Bahn of Runge-Lenz vector')
plt.savefig('Runge_Lenz' + str(n_orbit) + '.png', fmt='png', dpi=200)
# plt.show()

plt.figure()
plt.plot(t, angularMom_rk2[2], label='RK2')
plt.plot(t, angularMom_rk4[2], label='RK4')
plt.plot(t, angularMom_lf[2], label='LF')
plt.xlabel('time [orbits]')
plt.ylabel('total angular momentum')
plt.legend()
plt.title('Evolution of the angular momentum')
plt.savefig('angularMom' + str(n_orbit) + '.png', fmt='png', dpi=200)
# plt.show()

plt.figure()
plt.plot(0, 0, marker='o', markersize=3, color="red", label='Star')
plt.plot(x_rk2[:, 0], x_rk2[:, 1], label='RK2')
plt.plot(x_lf[:, 0], x_lf[:, 1], label='LF', linewidth=0.1)
plt.xlabel('x [AU]')
plt.ylabel('y [AU]')
plt.legend()
plt.title('solution curve of the kepler problem')
plt.savefig('lf_vs_rk2' + str(n_orbit) + '.png', bbox_inches='tight', dpi=254)
# plt.show()

plt.figure()
plt.plot(0, 0, marker='o', markersize=3, color="red", label='Star')
plt.plot(x_rk4[:, 0], x_rk4[:, 1], label='RK4')
plt.plot(x_lf[:, 0], x_lf[:, 1], label='LF', linewidth=0.1)
plt.xlabel('x [AU]')
plt.ylabel('y [AU]')
plt.legend()
plt.title('solution curve of the kepler problem')
plt.savefig('lf_vs_rk4' + str(n_orbit) + '.png', bbox_inches='tight', dpi=254)
# plt.show()
