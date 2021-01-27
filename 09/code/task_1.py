import matplotlib.pyplot as plt
import numpy as np

from advection import main as advection

x_N = 100
L = 10
dx = L/x_N

x = np.linspace(-L/2-dx, L/2+dx, num=x_N+2)
q_0 = (x - np.abs(x))/(2*x)


def plot(q, task, scheme='upwind', ts=[0, 250, 500]):
    plt.figure(figsize=(6, 4))

    colors = ['green', 'yellow', 'red']
    for idx, t in enumerate(ts):
        plt.plot(x, q[t], label=f"t={t}", color=colors[idx])

    plt.xticks([-L/2, 0, L/2], ['$-1/2$', 0, '1/2'])
    plt.xlabel('x/L')
    plt.ylabel('q(x)')
    # plt.xlim(-L, L)

    plt.legend()
    plt.savefig(f"../figures/{scheme}_{task}.png")
    plt.close()


# exercise 01, part 1, 2, 3
for idx, scheme in enumerate(['symmetric', 'upwind', 'downwind']):
    q = advection(q_0, scheme=scheme, t_N=500)
    plot(q, idx+1, scheme=scheme)

# exercise 01, part 4, 5
q = advection(q_0, boundary_conditions=[.5, 0], t_N=10000)
plot(q, 4, ts=[0, 1000, 10000])
q = advection(q_0, boundary_conditions=[1, .5], t_N=10000)
plot(q, 5, ts=[0, 1000, 10000])

# exercise 01, part 6, 7
q = advection(q_0, t_N=100)
plot(q, '6_0', ts=[3])
q = advection(q_0, t_N=1000)
plot(q, 6, ts=[3])
q = advection(q_0, t_N=10)
plot(q, 7, ts=[3])
