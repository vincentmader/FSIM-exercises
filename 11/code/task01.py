import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from tqdm import tqdm

from source import Grid, Pars, time_loop


EPSILON = 1e-4
SIGMA = 0.2

# initialize parameters
pars = Pars()
pars.Nx = 100
pars.x1 = -1
pars.x2 = 1
pars.cs = 1
pars.cfl = 0.4

# intitial conditions
x = np.linspace(pars.x1, pars.x2, pars.Nx)
rho_0 = 1 + EPSILON * np.exp(-x**2 / (2*SIGMA**2))
u_0 = np.array([0] * pars.Nx)


# run integration
def integrate(tmax):
    pars.tmax = tmax

    # create grid and set initial conditions
    grid = Grid(pars)
    grid.cons = np.array([rho_0, u_0])

    # run
    time_loop(grid, pars)
    rho, u = grid.cons
    return rho, u


def find_tcs():
    rhos = []
    for tmax in tqdm(np.linspace(0, 25, 100)):
        rho, u = integrate(tmax)
        rhos.append(rho[int(pars.Nx / 2)])  # get rho(x=0)

    plt.figure(figsize=(7, 4))
    plt.plot(rhos)
    plt.xlabel('$t$')
    plt.ylabel(r'$\rho(x=0,t)$')
    plt.savefig('../figures/sound_crossing_time_scale.pdf')
    plt.close()

    # get positions of maxima, the determine t_cs
    max_ind = argrelextrema(np.array(rhos), np.greater)[0]
    tcs = np.mean(np.diff(max_ind))
    return tcs


# tcs = find_tcs()
tcs = 7.72727272727272727

for i in tqdm(range(11)):
    tmax = i * tcs
    rho, u = integrate(tmax)
    label = r'$t_{max}=' + str(i) + '\cdot t_{c_s}$'
    label = r'$t_{max}=0$' if not i else label
    plt.xlim(x[0], x[-1])
    plt.plot(x, rho, label=label)

plt.legend()
plt.savefig('../figures/density_evolution.pdf')
plt.close()

E_kin = []
for i in tqdm(range(11)):
    tmax = i * tcs
    rho, u = integrate(tmax)
    E_kin.append(np.sum(rho * u**2 / 2))

plt.scatter(range(11), E_kin)
plt.xlabel('time $t/t_{c_s}$')
plt.ylabel(r'kinetic energy $E_{kin}}$')
plt.savefig('../figures/energy_evolution.pdf')
plt.close()
