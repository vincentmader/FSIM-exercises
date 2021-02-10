from source import *

x_Nx = []
y_L2 = []

for Nx in numpy.logspace(2, 3, 10):

    p = Pars()

    p.Nx = int(Nx)
    p.x1 = 0.
    p.x2 = 1.
    p.cs = 1.
    p.cfl = 0.4
    p.tmax = 1.

    g = Grid(p)

    A = 1.e-6
    g.cons[i_rho, 1:-1] = 1.0 + A*numpy.sin(2*pi*g.xc)
    g.cons[i_rhou, 1:-1] = A*(-1.)*numpy.sin(2*pi*g.xc)

    cons_0 = numpy.copy(g.cons)

    time_loop(g, p)

    err = numpy.sum(numpy.abs(cons_0[:, 1:-1]-g.cons[:, 1:-1]))/g.Nx
    L2 = (numpy.sum(err**2))**0.5

    x_Nx.append(Nx)
    y_L2.append(L2)


Nx = numpy.array(x_Nx)
L2 = numpy.array(y_L2)
lin = L2[0]*(Nx[0]/Nx)

plot(Nx, lin, label=r'$o(\Delta x)$', color='black', ls='--')
scatter(Nx, L2, label='HLL', color='red')
xlabel('Nx')
ylabel(r'$L_2$')
yscale('log')
xscale('log')
title('CFL=%.2f' % (p.cfl))
legend(frameon=False)
show()
