import numpy
from matplotlib.pyplot import *
from math import pi


# indices for conservative vars
i_rho = 0
i_rhou = 1


# ------------------------------------------


# physical fluxes (isothermal euler)
def euler_flux(grid, pars, cons_rec):
    f = numpy.zeros((2, grid.Nx-1))
    # print(i_rho, i_rhou)
    f[i_rho, :] = cons_rec[i_rhou, :]
    f[i_rhou, :] = cons_rec[i_rhou, :]**2/cons_rec[i_rho, :] \
        + cons_rec[i_rho, :]*pars.cs**2

    return f

# ------------------------------------------


# Pars class to store initial parameters
class Pars:
    def __init__(self):
        self.Nx = None
        self.x1 = None
        self.x2 = None
        self.cs = None
        self.cfl = None
        self.tmax = None

# ------------------------------------------


# grid class: contains all the variables and functions
# used to evolve the system
class Grid:

    # setup the system
    def __init__(self, pars):

        self.Nx = pars.Nx
        self.dx = (pars.x2-pars.x1)/self.Nx
        self.xc = numpy.linspace(
            pars.x1+self.dx/2., pars.x2-self.dx/2., self.Nx)
        self.cons = numpy.zeros((2, self.Nx+2))
        self.time = 0.
        self.dt = None
        self.i_model = 0

    # function to get dt given by CFL condition
    def get_dt(self, pars):
        u = self.cons[1, 1:-1] / self.cons[0, 1:-1]
        cs = pars.cs
        self.dt = pars.cfl*self.dx / numpy.max(numpy.abs(u)+cs)

    # function to apply periodic BCs
    def apply_periodic_bcs(self, pars):
        self.cons[:, 0] = self.cons[:, -2]
        self.cons[:, -1] = self.cons[:, 1]

    # function to perform constant reconstruciton
    # (returns left and right states)
    def reconstruct(self, pars):
        return self.cons[:, :-1], self.cons[:, 1:]  # left-right states

    # rk1 time marching scheme
    def rk1_update(self, pars, R):
        self.cons[:, 1:-1] -= R[:, :]*self.dt


# ------------------------------------------


# function for main time loop
def time_loop(grid, pars):

    while(grid.time < pars.tmax):

        grid.get_dt(pars)
        grid.apply_periodic_bcs(pars)
        consL, consR = grid.reconstruct(pars)
        flux = hll_riemann(grid, pars, consL, consR)
        R = (flux[:, 1:]-flux[:, :-1])/grid.dx
        grid.rk1_update(pars, R)
        grid.time += grid.dt
        grid.i_model += 1


# hll flux
def hll_riemann(grid, pars, L, R):

    fL = euler_flux(grid, pars, L)
    fR = euler_flux(grid, pars, R)
    f = numpy.zeros_like(fL)
    uL = L[i_rhou, :]/L[i_rho, :]
    uR = R[i_rhou, :]/R[i_rho, :]
    c = pars.cs
    SL = numpy.minimum(uL, uR) - c
    SR = numpy.maximum(uL, uR) + c

    kk_L = numpy.where(SL >= 0.)
    kk_star = numpy.where((SL < 0.) & (SR > 0.))
    kk_R = numpy.where(SR <= 0.)

    f[:, kk_L] = fL[:, kk_L]
    f[:, kk_star] = (
        SR[kk_star]*fL[:, kk_star] -
        SL[kk_star]*fR[:, kk_star] +
        SL[kk_star]*SR[kk_star] *
        (R[:, kk_star]-L[:, kk_star])
    ) / (SR[kk_star]-SL[kk_star])
    f[:, kk_R] = fR[:, kk_R]

    return f
