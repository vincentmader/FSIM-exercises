import matplotlib.pyplot as plt
import numpy as np


# load data
data = np.loadtxt('../MolDyn/output_T80.txt', skiprows=1)

time = [i[0] for i in data]
# E1 = [i[1] for i in data]
E2 = [i[2] for i in data]
E3 = [i[3] for i in data]
E4 = [i[4] for i in data]

# plot
plt.figure(figsize=(8, 4))

# plt.plot(time, E1, label='column 1')
plt.plot(time, E2, label=r'$E_{kin}$')
plt.plot(time, E3, label=r'$E_{pot}$')
plt.plot(time, E4, label=r'$E_{tot}$')
plt.plot(time, [0] * len(time), '--', color='grey')

plt.title('evolution of total energy over 20000 integration steps')
plt.xlabel(r'$t/\tau$')
plt.ylabel(r'$E/\sigma$')
plt.xlim(time[0], time[-1])
plt.legend(loc='upper left')

plt.savefig('../figures/energy.pdf')
