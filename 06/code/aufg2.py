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
    lenk = len(list(k))
    kLapl =np.zeros((lenk, lenk),dtype=complex)
    for i in range(lenk):
        for j in range(lenk):
            if (k[i] == 0) and (k[j]==0):
                continue
            kLapl[i,j] = -4 * np.pi * 1/(k[i]*k[j])
    # kinv[np.isinf(kinv)] = 0
    # apply Laplace in fourierspace
    # kLapl = -4* np.pi *np.tensordot(kinv, kinv, axes=0)
    kDen = ft.fft2(den)
    kpot = kLapl * kDen
    # ift to get potential and Force
    pot = np.real(ft.ifft2(kpot))
    return pot


def initialize_particles(r_min, r_max, N=100):
    # assemble 100 testparticles
    randNo = np.random.uniform(size=(N,2))
    testpart = np.zeros((N,2))
    testpart[:,0]= pos[0] + r_min * (r_max/r_min) ** randNo[:,0] * np.sin(2* np.pi*randNo[:,1])
    testpart[:,1]= pos[1] + r_min * (r_max/r_min) ** randNo[:,0] * np.cos(2* np.pi*randNo[:,1])
    testpart[testpart<0] += 1
    testpart[testpart>1] -= 1
    return testpart


# initalize data
NGrid = 256
x_1d = np.linspace(0,1,NGrid, endpoint=False) # Endpoint False, since periodic
# grid for plotting
x, y = np.meshgrid(x_1d, x_1d)
#L=1
r_min = 0.3 / NGrid
r_max = 0.5

pos = np.array([0.45354, 0.19182])
pot = calc_potential(x_1d, pos)
Forcx, Forcy = np.gradient(-pot,1/NGrid)
# get random particles
testpart = initialize_particles(r_min, r_max)
# 2D interpolation for forces
f_x = spinter.interp2d(x_1d, x_1d, Forcx)
f_y = spinter.interp2d(x_1d, x_1d, Forcy)





a_all = np.zeros(1000)
r_all = np.zeros(1000)
# position of mass
for i in range(10):
    pos = np.random.uniform(size=(2))
    pot = calc_potential(x_1d, pos)
    Forcx, Forcy = np.gradient(-pot,1/NGrid)
    # get random particles
    testpart = initialize_particles(r_min, r_max)
    # 2D interpolation for forces
    f_x = spinter.interp2d(x_1d, x_1d, Forcx)
    f_y = spinter.interp2d(x_1d, x_1d, Forcy)

    acc_x = f_x(testpart[:,0], testpart[:,1])
    acc_y = f_y(testpart[:,0], testpart[:,1])
    a_as = np.sqrt(np.diag(acc_x) ** 2 + np.diag(acc_y) ** 2)
    r_all[i*100:(i+1)*100] = np.sqrt(testpart[:,0]**2 + testpart[:,1]**2)
    a_all[i*100:(i+1)*100] = a_as


'''
cmap = plt.get_cmap('PiYG')
fig, ax0 = plt.subplots(nrows=1)
im = ax0.pcolormesh(x, y, density(x_1d,pos))
fig.colorbar(im, ax=ax0)
ax0.set_title('pcolormesh with levels')
fig.tight_layout()
'''
# plt.show()
plt.figure()
plt.plot(r_all, a_all, '.', label="acc")
plt.plot(r_all, 1/r_all, label="1/r")
plt.plot(r_all, 1/NGrid*r_all/r_all,label="L/N")
plt.legend()
plt.title("acceleration vs radius")
plt.xscale("log")
plt.yscale("log")
plt.ylim(1e-4, 1e2)
plt.savefig("../figures/acc2.pdf")
# plt.show()

print('Done.')
