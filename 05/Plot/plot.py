import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("../MolDyn/output_T80.txt", usecols=(0,2,3,4), skiprows=1)
plt.plot(data[:,0],data[:,1]/data[0,1], label="Ekin")
plt.plot(data[:,0],data[:,2]/(60*data[0,2]), label="Epot")
plt.plot(data[:,0],data[:,3]/data[0,3], label="Eges")
plt.legend()
plt.title("Energy")
plt.xlabel("t/t'")
plt.ylabel("E/sigma")
# plt.savefig("Energy.png")
# plt.show()

n=1000
mu = np.linspace(0,100,n)
means = []
vas = []
for i in range(n):
    Eges = data[:,1] + mu[i] * data[:,2]
    means.append(np.mean(Eges))
    vas.append(np.var(Eges))
plt.figure()
plt.plot(mu, means)
plt.plot(mu, vas)
plt.show()
print("Done.")
