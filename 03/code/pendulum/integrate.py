import json

from numpy import sin, cos, pi
from scipy import integrate

from config import *


def f(t, y):
    phi1 = y[0]
    phi2 = y[1]
    q1 = y[2]
    q2 = y[3]

    dphi = phi1-phi2
    M = m1 + m2

    f1 = (q1/(M*l1**2)-cos(dphi)/(M*l1*l2)*q2) / (1-m2/M*cos(dphi))
    f2 = q2/(m2*l2**2)-l1/l2*f1*cos(dphi)
    f3 = -M * g * l1 * sin(phi1)
    f4 = -m2 * g * l2 * sin(phi2)

    return [f1, f2, f3, f4]


def main():
    rk = integrate.RK23(f, t0, y0, t_bound=1e8)

    ys, Es = [], []
    for step_idx in range(nr_of_iterations):
        rk.step()
        # print(rk.y)

        phi1 = rk.y[0]
        phi2 = rk.y[1]
        q1 = rk.y[2]
        q2 = rk.y[3]

        y = [phi1, phi2, q1, q2]
        ys.append(y)

        dotphi1 = f(0, y)[0]
        dotphi2 = f(0, y)[1]
        E = m1/2*(l1*dotphi1)**2 + m2/2 * (
            (l1*dotphi1)**2 + (l2*dotphi2)**2 +
            2*l1*l2*dotphi1*dotphi2*cos(phi1-phi2) +
            m1*g*l1*(1-cos(phi1)) +
            m2*g*l1*(1-cos(phi1) + l2*(1-cos(phi2)))
        )
        Es.append(E)

    with open('./ys.json', 'w') as fp:
        json.dump(ys, fp)
    with open('./Es.json', 'w') as fp:
        json.dump(Es, fp)
    return ys


if __name__ == "__main__":
    main()
