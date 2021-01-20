import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def linear(x, a, b):
    return a * x + b


N = np.array([2.5, 5, 10, 20])*1000
tTree = np.array([24.8, 55.6, 198, 598])
tNsqr = np.array([46, 188, 1455, 4666])

Topt, Tcov = curve_fit(linear, np.log(N), np.log(tTree))
Nopt, Ncov = curve_fit(linear, np.log(N), np.log(tNsqr))

print(Topt)
print(Nopt)
ytos = 60*60*24*365
print("Tree(1e10)=", np.exp(linear(np.log(1e10), Topt[0], Topt[1]))/ytos)
print("Nsqr(1e10)=", np.exp(linear(np.log(1e10), Nopt[0], Nopt[1]))/ytos)

plt.figure(figsize=(7, 5))
# plt.title("execution time vs. particle number")
plt.xlabel("particle number")
plt.ylabel("execution time [s]")

plt.xscale('log')
plt.yscale('log')
# plt.gca().get_xaxis().get_major_formatter().labelOnlyBase = False
# plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.gca().set_xticks([5e3, 1e4, 2e4])

plt.scatter(N, tTree, label="tree method", color='blue', s=20)
plt.scatter(N, tNsqr, label="direct method", color='red', s=20)

x = range(1, int(max(100*N)))
plt.plot(x, np.exp(linear(np.log(x), Topt[0], Topt[1])), color='blue')
plt.plot(x, np.exp(linear(np.log(x), Nopt[0], Nopt[1])), color='red')

plt.xlim(.5*min(N), 2*max(N))
plt.ylim(5, 10**5)
plt.legend(loc='upper left')
plt.savefig("runtimes.png")

# plt.show()
