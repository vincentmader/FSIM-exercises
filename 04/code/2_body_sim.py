from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import RK23, RK45


G = 1
M_sun = 1
M_star = M_sun
M_planet = 1e-3 * M_sun

t_0 = 0
x_0 = np.array([1, 0, 0])
v_0 = np.array([0, .5, 0])


def norm(x):
    return np.sqrt(sum([i**2 for i in x]))


def a(x):
    return -G * M_star * x / norm(x)**3


def rk_integrate(x_0, v_0, dt, steps, order=2):

    # define derivative function
    def f(t, y):
        x = np.array(y[:3])
        v = np.array(y[3:])

        dv = a(x)
        dx = v
        return list(dx) + list(dv)

    y_0 = list(x_0) + list(v_0)
    # initialize integrator (either Rk2 or Rk4)
    if order == 2:
        rk_integrator = RK23(
            f, t_0, y0=y_0, t_bound=dt*steps, first_step=dt, max_step=dt
        )
    elif order == 4:
        rk_integrator = RK45(
            f, t_0, y0=y_0, t_bound=dt*steps, first_step=dt, max_step=dt
        )

    # iterate and return
    ys = []
    for _ in tqdm(range(steps)):
        rk_integrator.step()
        ys.append(rk_integrator.y)

    return np.array(ys)


def leapfrog_integrate(x_0, v_0, dt, steps):
    x, v = x_0, v_0

    def leapfrog_step(x, v):
        new_v = v + a(x) * dt / 2
        new_x = x + new_v * dt / 2
        return new_x, new_v

    xs, vs = [], []
    for _ in tqdm(range(steps)):
        x, v = leapfrog_step(x, v)
        xs.append(x)
        vs.append(v)

    return xs, vs


def plot_energies(xs, vs):
    E_kins, E_pots = [], []
    for idx, x in enumerate(xs):
        v = vs[idx]

        E_kin = M_planet / 2 * norm(v)**2
        E_pot = -G * M_star * M_planet / norm(x)

        E_kins.append(E_kin)
        E_pots.append(E_pot)

    E_kins = np.array(E_kins)
    E_pots = np.array(E_pots)
    E_tots = E_kins + E_pots
    E0 = E_tots[0]

    plt.subplot(121)

    plt.plot(E_kins, label=r'$E_{kin}$', color='green')
    plt.plot(E_pots, label=r'$E_{pot}$', color='red')
    plt.plot(E_tots, label=r'$E_{total}$', color='black')
    plt.legend(loc='lower left')

    plt.subplot(122)
    plt.plot(
        (E_tots-E0) / E0 * 100, label=r'$\frac{E-E_0}{E_0}\cdot 100$',
        color='black'
    )
    # plt.gca().ticklabel_format(axis='y', style='sci')
    plt.gca().yaxis.tick_right()
    plt.legend(loc='lower right')


# def plot_energy_error(xs, vs, label=''):
#     E_kins, E_pots = [], []
#     for idx, x in enumerate(xs):
#         v = vs[idx]

#         E_kin = M_planet / 2 * norm(v)**2
#         E_pot = -G * M_star * M_planet / norm(x)

#         E_kins.append(E_kin)
#         E_pots.append(E_pot)

#     E_kins = np.array(E_kins)
#     E_pots = np.array(E_pots)
#     E_tots = E_kins + E_pots
#     E0 = E_tots[0]

#     plt.plot(
#         (E_tots-E0) / E0 * 100, label=r'$\frac{E-E_0}{E_0}\cdot 100$',
#         color='black'
#     )
#     plt.legend(loc='lower right')


def plot_orbit(xs, linewidth=1):
    x = [i[0] for i in xs]
    y = [i[1] for i in xs]

    circ = plt.Circle((0, 0), 1e-2, color='k')
    plt.gca().add_artist(circ)
    plt.gca().set_aspect('equal', adjustable='box')

    plt.plot(x, y, linewidth=linewidth)
    plt.xlabel(r'$x$ coordinate')
    plt.ylabel(r'$y$ coordinate')


def main():

    # fig = plt.figure(figsize=(6, 4))
    fig = plt.figure(figsize=(8, 4))

    print('Leapfrog 1')
    xs, vs = leapfrog_integrate(x_0, v_0, dt=1e-2, steps=int(535))
    plot_orbit(xs)
    plt.savefig('../figures/task1_1_orbit_lf.pdf')
    fig.clear()
    plot_energies(xs, vs)
    plt.savefig('../figures/task1_1_energies_lf.pdf')
    fig.clear()

    print('Leapfrog 2')
    xs, vs = leapfrog_integrate(x_0, v_0, dt=1e-2, steps=int(1e5))
    plot_orbit(xs, linewidth=0.01)
    plt.savefig('../figures/task1_1_orbit_lf_100.pdf')
    plot_energies(xs, vs)
    plt.savefig('../figures/task1_1_energies_lf_100.pdf')
    fig.clear()

    print('Leapfrog 3')
    xs_lf, vs_lf = leapfrog_integrate(x_0, v_0, dt=1e-2, steps=int(5e3))
    plot_orbit(xs_lf)
    plt.savefig('../figures/task1_1_orbit_lf_test.pdf')
    plot_energies(xs_lf, vs_lf)
    plt.savefig('../figures/task1_1_energies_lf_test.pdf')
    fig.clear()

    print('Runge-Kutta 1')
    y = rk_integrate(x_0, v_0, dt=1e-2, steps=int(5e3), order=2)
    xs_rk2 = [i[:3] for i in y]
    vs_rk2 = [i[3:] for i in y]
    plot_orbit(xs_rk2)
    plt.savefig('../figures/task1_1_orbit_rk2.pdf')
    fig.clear()
    plot_energies(xs_rk2, vs_rk2)
    plt.savefig('../figures/task1_1_energies_rk2.pdf')
    fig.clear()

    print('Runge-Kutta 2')
    y = rk_integrate(x_0, v_0, dt=1e-2, steps=int(5e3), order=4)
    xs_rk4 = [i[:3] for i in y]
    vs_rk4 = [i[3:] for i in y]
    plot_orbit(xs_rk4)
    plt.savefig('../figures/task1_1_orbit_rk4.pdf')
    fig.clear()
    plot_energies(xs_rk4, vs_rk4)
    plt.savefig('../figures/task1_1_energies_rk4.pdf')
    fig.clear()

    # print('together')
    # plot_energy_error(xs_lf, vs_lf, label='leapfrog')
    # plot_energy_error(xs_rk2, vs_rk2, label='Rk2')
    # plot_energy_error(xs_rk4, vs_rk4, label='Rk4')
    # plt.savefig('../figures/energy_errors.pdf')

# t_bound = steps * dt


if __name__ == "__main__":
    main()
