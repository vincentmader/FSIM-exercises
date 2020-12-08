import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("../MolDyn/output_T80.txt", usecols=(0,4), skiprows=1)
plt.plot(data[:,0],data[:,1])
plt.title("Energy")
plt.xlabel("t/t'")
plt.ylabel("E/sigma")
plt.savefig("Energy.png")
# plt.show()
print("Done.")
