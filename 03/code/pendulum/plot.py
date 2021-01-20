import json

import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin, pi

from config import *


def plot_pendulum():
    with open('./ys.json') as fp:
        ys = json.load(fp)

    for step_idx, y in enumerate(ys):
        phi1 = y[0]
        phi2 = y[1]
        q1 = y[2]
        q2 = y[3]

        phi1 -= pi / 2
        phi2 -= pi / 2

        x1 = l1 * cos(phi1)
        x2 = l1 * cos(phi1) + l2 * cos(phi2)
        y1 = l1 * sin(phi1)
        y2 = l1 * sin(phi1) + l2 * sin(phi2)

        plt.figure(figsize=(4, 4))
        plt.scatter([x1], [y1])
        plt.scatter([x2], [y2])
        plt.plot([0, x1], [0, y1], color='black')
        plt.plot([x1, x2], [y1, y2], color='black')
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        idx = f'0{step_idx}' if step_idx < 10 else step_idx
        idx = f'0{idx}' if step_idx < 100 else step_idx
        idx = f'0{idx}' if step_idx < 1000 else step_idx
        plt.savefig(f'../../figures/{idx}.png')
        plt.close()

    with open('./ys.json') as fp:
        ys = json.load(fp)


def plot_energy():
    with open('./Es.json') as fp:
        Es = json.load(fp)

    E0 = Es[0]

    x = range(len(Es))
    y = (np.array(Es) - E0) / E0

    plt.figure(figsize=(4, 4))
    plt.plot(x, y)
    plt.xlabel('time step')
    plt.ylabel(r'energy discrepancy $(E-E_0)/E_0$')
    plt.savefig('../../energies_rk23.pdf')


if __name__ == "__main__":
    plot_energy()
    # plot_pendulum()
