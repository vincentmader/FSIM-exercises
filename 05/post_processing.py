import numpy
from matplotlib.pyplot import *
import os

i_x = 0
i_y = 1
i_z = 2

#EX1:
#time profiling (let's plot the time evolution of rel err E)


i_min = 0
i_max = 99

E_list = []
t_list = []

for i in range(i_min,i_max):

      data = numpy.load('%d.npz'%(i))
       
      coord = data['coord']
      vel   = data['vel']
      V     = data['V']
      K     = data['K']
      E     = data['E']
      t     = data['t']
      Np    = data['Np']

      t_list.append(t)
      E_list.append(E)   

E = numpy.array(E_list)

plot(t_list,numpy.log10(numpy.abs((E-E[0])/E[0])))
xlabel('t')
ylabel(r'$log_{10} \ | \frac{E(t)-E(0)}{E(0)} |$')
show()



#EX2:
#scatter plot at fixed time

i = 90

data = numpy.load('%d.npz'%(i))
       
coord = data['coord']
vel   = data['vel']
V     = data['V']
K     = data['K']
E     = data['E']
t     = data['t']
Np    = data['Np']

scatter(coord[:,i_x],coord[:,i_z],color='black',marker='x')

xlabel('x')
ylabel('z')
title('t=%.5f'%(t))
show()


#EX3:
#velocity distribution at fixed time


hist(vel[:,i_x],bins=int(Np**0.5),label=r'$v_x$',alpha=0.6)
hist(vel[:,i_y],bins=int(Np**0.5),label=r'$v_y$',alpha=0.6)
hist(vel[:,i_z],bins=int(Np**0.5),label=r'$v_z$',alpha=0.6)

legend(frameon=False)

xlabel('v')
ylabel('counts')
show()




