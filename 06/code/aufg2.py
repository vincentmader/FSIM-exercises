import numpy as np
import matplotlib.pyplot as plt

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

x_1d = np.linspace(0,1,10, endpoint=False)
x, y = np.meshgrid(x_1d, x_1d)
pos = np.array([0.45354, 0.19182])
den = density(x_1d,pos)
print(den)
print('Done.')
