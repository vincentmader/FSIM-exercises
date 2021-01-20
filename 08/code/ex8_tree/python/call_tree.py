from tree import *
from random import *
import time
from copy import *
from math import sqrt
import sys

'''
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
'''


def call_tree(N, angle):
    print('N = {}, angle = {} \n'.format(N, angle))
    particles = np.zeros((N, 3))
    for i in range(N):
        x = random()
        y = random()
        z = random()
        particles[i] = np.array([x, y, z])

    q = TreeClass(particles)
    q.insertallparticles()
    q.computemultipoles(0)

    print("starting tree gravity")
    t0 = time.time()
    q.allgforces(angle)
    t1 = time.time()
    treegrav_dt = t1-t0
    print("done in " + str(treegrav_dt) + " seconds")
    print("the mean number of interactions is {}\n".format(np.mean(q.interactions)))

    fapprox = deepcopy(q.forces)

    print("starting N^2 gravity")
    t0 = time.time()

    # ... TO BE FILLED IN ...
    acc = np.zeros((len(particles), 3))
    for index, body in enumerate(particles):  # itterate over all other bodies
        a = 0
        for j in range(len(particles)):
            if index != j:
                r = np.linalg.norm(body - particles[j])
                tmp = 1 / r**3
                a += tmp*(body - particles[j])
        acc[index] = a

    t1 = time.time()
    fullgrav_dt = t1-t0
    print("done in " + str(fullgrav_dt) + " seconds\n")

    fexact = acc  # m=1 => F = a

    # ... TO BE FILLED IN ...

    rel_err = np.mean(np.abs((fapprox-fexact)/fexact))*100
    drel = np.std((fapprox-fexact)/fexact)*100/np.sqrt(N)

    print(r"the relative error is: {:.2f} \pm {:.2f}%".format(rel_err, drel))


# for N in [5000]: # ,10000,20000,40000]: #
# for angle in [0.2, 0.4,0.8]:

call_tree(
    int(sys.argv[1]),   # particle number (integer)
    float(sys.argv[2])  # opening angle (float between 0 and 1)
)
print('---------------------------------------------------\n')
