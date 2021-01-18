from tree import *
from random import *
import time
from copy import *
from math import sqrt

#
# Create a set of randomly positioned particles
# For convenience we assume all masses to be 1.
# If we have in reality another mass, we can simply
# rescale our answers.
#
nparticles = 100
particles = []
for i in range(nparticles):
    x = random()
    y = random()
    z = random()
    particles.append([x,y,z])

#
# Now create the tree
#
q=TreeClass(particles)
q.insertallparticles()
q.computemultipoles(0)


print "starting tree gravity"
t0 = time.time()
q.allgforces(0.8)
t1 = time.time()
treegrav_dt = t1-t0
print "done in "+str(treegrav_dt)+" seconds\n"

fapprox = deepcopy(q.forces)

print "starting N^2 gravity"
t0 = time.time()

# ... TO BE FILLED IN ...
print "Please replace this print statement with your own code"

t1 = time.time()
fullgrav_dt = t1-t0
print "done in "+str(fullgrav_dt)+" seconds\n"

fexact = deepcopy(q.forces)

# 
# Now compare the approximate and exact versions
#
# ... TO BE FILLED IN ...
print "Please replace this print statement with your own code"
