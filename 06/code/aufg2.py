import numpy as np
import matplotlib.pyplot as plt
import numpy.fft as ft
import scipy.interpolate as spinter
# asume quadratic mesh x

def density(x, pos):
    dx = x[1]-x[0]
    N = int(1/dx)   # L=1
    # calc partins in different cells with index of lower left cell
    flpos = pos/dx - 1/2
    index = np.array(np.floor(flpos), dtype=int)
    part = flpos - index
    # calc rho
    rho = np.zeros((N,N))
    rho[index[0], index[1]] = (1-part[0]) * (1-part[1])
    # calc different cases, when aprticle is near edge
    if index[0] == N-1 :
        if index[1] == N-1 :
            rho[0, 0] = (part[0]) * (part[1])
            rho[0, index[1]] = part[0] * (1-part[1])
            rho[index[0], 0] = (1-part[0]) * part[1]
        else:
            rho[0, index[1]+1] = (part[0]) * (part[1])
            rho[0, index[1]] = part[0] * (1-part[1])
            rho[index[0], index[1]+1] = (1-part[0]) * part[1]

    else:
        if index[1] == N-1 :
            rho[index[0]+1, 0] = (part[0]) * (part[1])
            rho[index[0]+1, index[1]] = part[0] * (1-part[1])
            rho[index[0], 0] = (1-part[0]) * part[1]
        else:
            rho[index[0]+1, index[1]+1] = (part[0]) * (part[1])
            rho[index[0]+1, index[1]] = part[0] * (1-part[1])
            rho[index[0], index[1]+1] = (1-part[0]) * part[1]
    return rho

def calc_potential(x,pos):
    # calc density and forces
    den = density(x_1d,pos)
    # calc wavevectors and avoid muliply/add with infty
    k = ft.fft(x_1d)
    kinv = 1/k
    kinv[np.isinf(kinv)] = 0
    # apply Laplace in fourierspace
    kLapl = -4* np.pi *np.tensordot(kinv, kinv, axes=0)
    kDen = ft.fft2(den)
    kpot = kLapl * kDen
    # ift to get potential and Force
    pot = np.real(ft.ifft2(kpot))
    return pot


def initialize_particles(r_min, r_max, N=100):
    # assemble 100 testparticles
    randNo = np.random.uniform(size=(100,100))
    testpart = np.zeros((100,100))
    testpart[0]= pos[0] + r_min * (r_max/r_min) ** randNo[:,0] * np.sin(2* np.pi*randNo[:,1])
    testpart[1]= pos[1] + r_min * (r_max/r_min) ** randNo[:,0] * np.cos(2* np.pi*randNo[:,1])
    testpart[testpart<0] += 1
    testpart[testpart>1] -= 1
    return testpart


# initalize data
NGrid = 256
x_1d = np.linspace(0,1,NGrid, endpoint=False) # Endpoint False, since periodic
# grid for plotting
x, y = np.meshgrid(x_1d, x_1d)
# position of mass
pos = np.array([0.45354, 0.19182])


pot = calc_potential(x_1d, pos)
Forcx, Forcy = np.gradient(-pot,1/NGrid)


r_min = 0.3 / NGrid
r_max = 0.5

# 2D interpolation for forces
f_x = spinter.interp2d(x_1d, x_1d, Forcx)
f_y = spinter.interp2d(x_1d, x_1d, Forcy)

acc_x = f_x(testpart[0], testpart[1])
acc_y = f_y(testpart[0], testpart[1])
a_as = np.sqrt(acc_x ** 2 + acc_y ** 2)



print("Density =", den)
print("Potential = ", pot)
print("Force in x=", Forcx)
print("Force in y = ", Forcy)

print('Done.')
