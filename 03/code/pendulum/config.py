import math

from numpy import pi


g = 1
m1, m2 = .5, 1
l1, l2 = 2, 1
dt, t_max = .05, 100
nr_of_iterations = math.floor(t_max / dt)

t0 = 0
y0 = [50 / 180. * pi, -120 / 180. * pi, 0, 0]
