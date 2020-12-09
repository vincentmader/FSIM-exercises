import matplotlib.pyplot as plt
import numpy as np


# load data
data = np.loadtxt('../MolDyn/output_T80.txt', skiprows=1)

time = [i[0] for i in data]
E_kin = np.array([i[2] for i in data])
E_pot = np.array([i[3] for i in data])
E_tot = np.array([i[4] for i in data])

E_kin0, E_pot0, E_tot0 = E_kin[0], E_pot[0], E_tot[0]

# plot
plt.figure(figsize=(8, 4))

# plt.plot(time, E1, label='column 1')
plt.plot(time, E_kin, label=r'$E_{kin}$')
plt.plot(time, E_pot, label=r'$E_{pot}$')
plt.plot(time, E_tot, label=r'$E_{tot}$')
plt.plot(time, [0] * len(time), '--', color='grey')

plt.title('evolution of energies')
plt.xlabel(r'$t/\tau$')
plt.ylabel(r'$E/\epsilon$')
plt.xlim(time[0], time[-1])
plt.legend(loc='upper left')

plt.savefig('../figures/energy.pdf')

plt.figure(figsize=(8, 4))
plt.plot(time, (E_tot - E_tot0) / E_tot0, label=r'$E_{tot}$')
plt.title('evolution of relative deviation of total energy')
plt.xlabel(r'$t/\tau$')
plt.ylabel(r'$\Delta E/(E_0\epsilon)$')
plt.xlim(time[0], time[-1])
plt.legend(loc='upper left')

plt.savefig('../figures/relative_energy.pdf')
