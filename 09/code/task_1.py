import matplotlib.pyplot as plt
import numpy as np

from advection import main as advection

x_N = 100
L = 10
dx = L/x_N

x = np.linspace(-L/2-dx, L/2+dx, num=x_N+2)
q_0 = (x - np.abs(x))/(2*x)


def plot(q, task, scheme='upwind', ts=[0, 100], xlims=None):
    plt.figure(figsize=(6, 4))

    colors = ['green', 'red']
    for idx, t in enumerate(ts):
        plt.plot(x, q[t], label=f"t={t}", color=colors[idx])

    plt.xlabel('x/L')
    plt.ylabel('q(x)')
    if xlims:
        plt.xlim(xlims[0], xlims[1])
        plt.xticks([xlims[0], 0, xlims[1]], [xlims[0]/L, 0, xlims[1]/L])
    else:
        plt.xticks([-L/2, 0, L/2], ['$-1/2$', 0, '1/2'])

    plt.legend()
    plt.savefig(f"../figures/{scheme}_{task}.png")
    plt.close()


# exercise 01, part 1, 2, 3
for idx, scheme in enumerate(['symmetric', 'upwind', 'downwind']):
    q = advection(q_0, scheme=scheme)
    plot(q, idx+1, scheme=scheme)

# exercise 01, part 4, 5
q = advection(q_0, boundary_conditions=[.5, 0])
plot(q, 4)
q = advection(q_0, boundary_conditions=[1, .5])
plot(q, 5)

# exercise 01, part 6, 7
xlims = [-.1*L, .1*L]
q = advection(q_0, t_N=100)
plot(q, '6_0', ts=[100], xlims=xlims)
q = advection(q_0, t_N=1000)
plot(q, 6, ts=[1000], xlims=xlims)
q = advection(q_0, t_N=10)
plot(q, 7, ts=[10], xlims=xlims)
