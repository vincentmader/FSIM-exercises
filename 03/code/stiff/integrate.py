import json

from numpy import sin, cos, pi
from scipy import integrate


kB = 1.38e-38
alpha = 10.
beta = -.5
T0 = 20000.
lamb0 = 10e-35
nH = 10e6

t0 = 0
Tinit = 10**7
y0 = [Tinit]
nr_of_iterations = 100


def f(t, y):
    def lamb(T):
        if T <= T0:
            return lamb0 * (T/T0) ** alpha
        else:
            return lamb0 * (T/T0) ** beta
    T = y[0]
    f = -2/(3*kB) * nH * lamb(T)
    return [f]


def main():
    rk = integrate.RK23(f, t0, y0, t_bound=1e8)

    Ts = []
    for step_idx in range(nr_of_iterations):
        rk.step()
        T = rk.y[0]
        if T < 6000:
            break
        Ts.append(T)

    with open('./Ts.json', 'w') as fp:
        json.dump(Ts, fp)
    return Ts


if __name__ == "__main__":
    main()
