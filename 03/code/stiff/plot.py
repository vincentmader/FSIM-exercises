import json

import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin, pi


def plot():
    with open('./Ts.json') as fp:
        Ts = json.load(fp)

    plt.figure(figsize=(8, 4))
    plt.semilogy(Ts)
    plt.xlabel('integration step')
    plt.ylabel('temperature [K]')
    plt.savefig('../../temperatures.pdf')


if __name__ == "__main__":
    plot()
