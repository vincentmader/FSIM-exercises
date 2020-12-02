import json
from random import uniform
from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np


G = 1.
steps = 50000

colors = ['blue', 'green', 'red']


def norm(vec):
    return np.sqrt(sum([i**2 for i in vec]))


class Planet():
    def __init__(self, r_0, v_0, m):
        self.r = r_0
        self.v = v_0
        self.m = m
        self.trajectory = []
        self.velocities = []

    def update_velocity(self, planets, dt):
        epsilon = 2 * len(planets)**(-1/3) / 10000
        for p in planets:
            if p == self:
                continue
            delta_r = p.r - self.r
            a = G * p.m * delta_r / (norm(delta_r)**3 + epsilon**3)
            self.v = np.add(self.v, a * dt)

        self.velocities.append(self.v)

    def update_position(self, dt):
        self.r = np.add(self.r, self.v * dt)
        self.trajectory.append(self.r)
        if self.r > 1e6:
            print('divergence!')
            input()


def create_2_body_system():
    r_10, v_10, m1 = np.array([-.5, 0, 0]), np.array([0, -.5, 0]), 1
    r_20, v_20, m2 = np.array([.5, 0, 0]), np.array([0, .5, 0]), 1

    p1 = Planet(r_10, v_10, m1)
    p2 = Planet(r_20, v_20, m2)

    return [p1, p2]


def create_3_body_system():
    r_10, v_10, m1 = np.array([-.5, 0, 0]), np.array([0, -.5, 0]), 1
    r_20, v_20, m2 = np.array([.5, 0, 0]), np.array([0, .5, 0]), 1
    r_30, v_30, m3 = np.array([1, 6, 2]), np.array([0, 0, 0]), .1

    p1 = Planet(r_10, v_10, m1)
    p2 = Planet(r_20, v_20, m2)
    p3 = Planet(r_30, v_30, m3)

    return [p1, p2, p3]


def create_30_body_system():
    planets = []
    for _ in range(30):
        valid_r, valid_v = False, False
        while not valid_r:
            x = uniform(-1, 1)
            y = uniform(-1, 1)
            z = uniform(-1, 1)
            if np.sqrt(x**2 + y**2 + z**2) <= 1:
                valid_r = True
        while not valid_v:
            vx = uniform(-.1, .1)
            vy = uniform(-.1, .1)
            vz = uniform(-.1, .1)
            if np.sqrt(vx**2 + vy**2 + vz**2) <= .1:
                valid_v = True

        r, v, m = np.array([x, y, z]), np.array([vx, vy, vz]), 1
        p = Planet(r, v, m)

        planets.append(p)

    return planets


def plot_system(planets):

    for idx, p in enumerate(planets):
        x = [i[0] for i in p.trajectory]
        y = [i[1] for i in p.trajectory]

        if len(planets) == 3:
            plt.xlabel(r'$y$ coordinate')
            plt.ylabel(r'$x$ coordinate')
            plt.plot(y, x, color=colors[idx])
        elif len(planets) == 30:
            plt.xlabel(r'$x$ coordinate')
            plt.ylabel(r'$y$ coordinate')
            plt.plot(y, x, color='black')
        else:
            plt.xlabel(r'$x$ coordinate')
            plt.ylabel(r'$y$ coordinate')
            plt.plot(x, y, color=colors[idx])

    steps = len(planets[0].trajectory)
    plt.title(
        f'evolution of {len(planets)} planets after {steps} iteration steps'
    )
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(f'../figures/task2_{len(planets)}body.pdf')


def plot_system_3D(planets):

    ax = plt.gcf().add_subplot(111, projection='3d')
    for idx, p in enumerate(planets):
        x = [i[0] for i in p.trajectory]
        y = [i[1] for i in p.trajectory]
        z = [i[2] for i in p.trajectory]

        ax.set_xlabel(r'$x$ coordinate')
        ax.set_ylabel(r'$y$ coordinate')
        ax.set_zlabel(r'$z$ coordinate')

        ax.plot(x, y, z)

        # plt.plot(y, x, color='black')

    steps = len(planets[0].trajectory)
    plt.title(
        f'3D evolution of {len(planets)} planets after {steps} iteration steps'
    )
    plt.savefig(f'../figures/task2_{len(planets)}body_3D_new.pdf')


def get_energy_evolution(planets):
    Es = []
    steps = planets[0].trajectory
    for idx, _ in enumerate(steps):
        for p in planets:
            v = p.velocities[idx]
            T = p.m / 2 * norm(v)**2
            V = 0
            for q in planets:
                if p is q:
                    continue
                d = norm(p.trajectory[idx] - q.trajectory[idx])
                V += G * p.m / d
        Es.append(T + V)

    return Es


def plot_energy_deviation(planets):
    Es = get_energy_evolution(planets)
    E0 = Es[0]

    plt.plot((Es-E0)/E0)
    plt.title(f'evolution of energy for {len(planets)} planets')
    plt.xlabel('iteration step')
    plt.ylabel(r'energy deviation $\frac{E_0-E}{E_0}}$')
    plt.savefig(f'../figures/task2_{len(planets)}body_energy_new.pdf')


def calculate_adaptive_dt(planets):
    ds, vs = [], []
    for p in planets:
        for q in planets:
            if p is q:
                continue
            ds.append(norm(p.r - q.r))
        vs.append(norm(p.v))
    d_min = min(ds)
    v_max = max(vs)
    return 0.1 * d_min / v_max


def run_system(planets, steps):
    for _ in tqdm(range(steps)):
        dt = calculate_adaptive_dt(planets)
        # dt = 1e-3
        for p in planets:
            p.update_velocity(planets, dt)
            p.update_position(dt)

    return planets


def main():

    # plt.figure(figsize=(8, 4))
    # planets = create_2_body_system()
    # plot_system(planets, steps=30000)
    # plt.close()

    # plt.figure(figsize=(8, 4))
    # planets = create_3_body_system()
    # plot_system(planets, steps=30000)
    # plt.close()

    planets = create_30_body_system()
    run_system(planets, steps)

    plt.figure(figsize=(8, 4))
    plot_system(planets)
    plt.close()

    plt.figure(figsize=(8, 4))
    plot_system_3D(planets)
    plt.close()

    plt.figure(figsize=(8, 4))
    plot_energy_deviation(planets)
    plt.close()


if __name__ == "__main__":
    main()
