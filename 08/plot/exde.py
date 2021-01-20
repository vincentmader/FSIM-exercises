import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def loglin(x,a,b):
    return a * x + b

N = np.array([2.5, 5, 10, 20])*1000
tTree = np.array([24.8, 55.6, 198, 598])
tNsqr = np.array([46, 188, 1455, 4666])
Topt, Tcov = curve_fit(loglin, np.log(N), np.log(tTree))
Nopt, Ncov = curve_fit(loglin, np.log(N), np.log(tNsqr))
print(Topt)
print(Nopt)
print("Tree(1e10)=", np.exp(loglin(np.log(1e10), Topt[0], Topt[1])))
print("Nsqr(1e10)=", np.exp(loglin(np.log(1e10), Nopt[0], Nopt[1])))
plt.plot(N, tTree, '.', label="Tree")
plt.plot(N, tNsqr, '.', label="exact")

plt.plot(N, np.exp(loglin(np.log(N), Topt[0], Topt[1])), "-")
plt.plot(N, np.exp(loglin(np.log(N), Nopt[0], Nopt[1])), "-")
plt.title("Runtimes ")
plt.xscale('log')
plt.yscale('log')
plt.xlabel("log(N)")
plt.ylabel("log(time/s)")
plt.legend()
plt.savefig("runtimes.png")
# plt.show()
