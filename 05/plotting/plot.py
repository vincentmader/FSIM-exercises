import matplotlib.pyplot as plt
import numpy as np


# load data
data = np.loadtxt('../MolDyn/output_T80.txt', skiprows=1)

time = [i[0] for i in data]
E1 = [i[1] for i in data]
E2 = [i[2] for i in data]
E3 = [i[3] for i in data]
E4 = [i[4] for i in data]

# plot
plt.figure(figsize=(8, 4))

plt.plot(time, E1, label='column 1')
plt.plot(time, E2, label='column 2')
plt.plot(time, E3, label='column 3')
plt.plot(time, E4, label='column 4')

plt.title('evolution of total energy')
plt.xlabel(r'$t/\tau$')
plt.ylabel(r'$E/\sigma$')
plt.legend(loc='upper left')

plt.savefig('../figures/energy.pdf')
