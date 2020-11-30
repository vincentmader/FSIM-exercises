from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np


G = 1.
dt = 1e-3
steps = 30000

colors = ['blue', 'green', 'red']


def norm(vec):
    return np.sqrt(sum([i**2 for i in vec]))


class Planet():
    def __init__(self, r_0, v_0, m):
        self.r = r_0
        self.v = v_0
        self.m = m
        self.trajectory = []

    def update_velocity(self, planets):
        for p in planets:
            if p == self:
                continue
            epsilon = 1e-6  # TODO
            delta_r = p.r - self.r
            a = G * p.m * delta_r / (norm(delta_r)**3 + epsilon**3)
            self.v = np.add(self.v, a * dt)

    def update_position(self):
        self.r = np.add(self.r, self.v * dt)
        self.trajectory.append(self.r)


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


def plot_system(planets):
    for _ in tqdm(range(steps)):
        for p in planets:
            p.update_velocity(planets)
            p.update_position()

    for idx, p in enumerate(planets):
        x = [i[0] for i in p.trajectory]
        y = [i[1] for i in p.trajectory]

        if len(planets) == 3:
            plt.xlabel(r'$y$ coordinate')
            plt.ylabel(r'$x$ coordinate')
            plt.plot(y, x, color=colors[idx])
        else:
            plt.xlabel(r'$x$ coordinate')
            plt.ylabel(r'$y$ coordinate')
            plt.plot(x, y, color=colors[idx])

    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(f'../figures/task2_{len(planets)}body.pdf')


def main():

    plt.figure(figsize=(8, 4))
    planets = create_2_body_system()
    plot_system(planets)
    plt.close()

    plt.figure(figsize=(8, 4))
    planets = create_3_body_system()
    plot_system(planets)
    plt.close()


if __name__ == "__main__":
    main()
