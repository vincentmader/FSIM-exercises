import numpy as np
import matplotlib.pyplot as plt
import numpy.fft as ft
# asume quadratic mesh x

def density(x, pos):
    dx = x[1]-x[0]
    N = int(1/dx)   # L=1
    print(N, dx)
    flpos = pos/dx - 1/2
#     loc = np.round( pos * N) / N
#    part = (pos-loc) * N   # part in both lower halfs
#    sign = np.sign(part)
#    print(part)
#    print(loc)
#    x_index = int(loc[0] * N)
#    y_index = int(lox[1] * N)
#    x_sign = part
#    loc[loc >= (N-1) * dx] -=

    index = np.array(np.floor(flpos), dtype=int)

    part = flpos - index
    rho = np.zeros((N,N))
    rho[index[0], index[1]] = (1-part[0]) * (1-part[1])
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
NGrid = 256
x_1d = np.linspace(0,1,NGrid, endpoint=False)
x, y = np.meshgrid(x_1d, x_1d)
pos = np.array([0.45354, 0.19182])
den = density(x_1d,pos)
k = ft.fft(x_1d)
kinv = 1/k
kinv[np.isinf(kinv)] = 0
# kinv[kinv==-inf] = 0
kLapl = -4* np.pi *np.tensordot(kinv, kinv, axes=0)
kDen = ft.fft2(den)
kpot = kLapl * kDen
pot = np.real(ft.ifft2(kpot))
Forcx, Forcy = np.gradient(-pot,1/NGrid)


print("Density =", den)
print("Potential = ", pot)
print("Force in x=", Forcx)
print("Force in y = ", Forcy)

print('Done.')
