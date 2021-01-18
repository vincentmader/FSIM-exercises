import numpy as np
from math import sqrt

#======================================================================
#                A SIMPLE TREE CODE FOR PARTICLES IN PYTHON 
#                          by C.P. Dullemond
#                                 2014
#              (based in part on a C-version of V. Springel)
#
#              NOTE: THIS VERSION IS INTENTIONALLY UNFINISHED!
#                    MUST BE FINISHED BY THE STUDENTS
#
# Example usage (setting up a random set of particles of mass 1):
#    
#    from tree import *
#    from random import *
#    nparticles = 100
#    particles = []
#    for i in range(nparticles):
#        x = random()
#        y = random()
#        z = random()
#        particles.append([x,y,z])
#
#    q=TreeClass(particles)
#    q.insertallparticles()
#    q.computemultipoles(0)
#    q.allgforces(0.8)
#
#======================================================================

#
# Define the class NodeClass
#
class NodeClass:
    def __init__(self):
        #
        # A flag telling whether this node is a branch (i.e. with children) or a leaf 
        #
        self.leaf = 1
        #
        # Identification numbers of the children (if not a leaf)
        #
        self.childrenids = np.zeros((2,2,2),dtype=int)
        #
        # The cell center
        #
        self.xc = [0.,0.,0.]
        #
        # The cell size 
        #
        self.size = 0.
        #
        # The center of mass
        #
        self.cm = [0.,0.,0.]
        #
        # Mass of this node
        #
        self.mass = 0.0
        #
        # The particle in this cell (-1 = no particle)
        #
        self.particleid = -1


#
# Define the class TreeClass
#
class TreeClass:
    def __init__(self,particles):
        #
        # List of nodes. Each node is from the class NodeClass (see above)
        #
        self.nodelist = []
        #
        # Add the first (top) node to the list
        #
        self.nodelist.append(NodeClass())
        #
        # Complete list of particles that we wish to organize with the tree.
        # Each particle in this list has 3 numbers: [x,y,z], where
        # x,y,z are the coordinates. The masses are all assumed to be 1.0
        #
        self.particles = particles
        #
        # Complete list of forces on the above particles. 
        # Each particle has 3 numbers: [fx,fy,fz]
        #
        self.forces = np.zeros((len(particles),3),dtype=float)
        #
        # If the particle list is not empty then we can calculate the 
        # box geometry of the top node
        #
        if len(self.particles) > 0:
            #
            # Min and max of all three coordinates. Ensure square box.
            # (Not the most elegant method though)
            #
            min  = np.amin(self.particles)
            max  = np.amax(self.particles)
            self.nodelist[0].size = (max-min)*1.1
            for coord in [0,1,2]:
                self.nodelist[0].xc[coord] = 0.5 * (min+max)
        #
        # Done for now, but keep in mind that the tree itself is not
        # yet finished: only the first node is finished.
        #

    #
    # Method to add a new (empty) node to the list
    #
    def createnode(self):
        #
        # Find the identification number for the new node
        #
        nodeid = len(self.nodelist)
        #
        # Append a node
        #
        self.nodelist.append(NodeClass())
        #
        # Return the identification number of the node
        #
        return nodeid

    #
    # Method for creating 2x2x2 children of a node
    # 
    def createchildren(self,nodeid):
        #
        # Works only if this node is not yet a parent
        #
        if self.nodelist[nodeid].leaf == 0:
            print "ERROR: Node already has children"
            quit()
        #
        # Promote this node to be a parent
        #
        self.nodelist[nodeid].leaf = 0
        #
        # Create the 2x2x2 children and link them
        #
        for iz in range(0,2):
            for iy in range(0,2):
                for ix in range(0,2):
                    #
                    # Create the child and get its ID number
                    #
                    childid = self.createnode()
                    #
                    # Link parent to child
                    #
                    self.nodelist[nodeid].childrenids[ix,iy,iz] = childid
                    #
                    # Compute the cell center of this child
                    #
                    size = self.nodelist[nodeid].size
                    self.nodelist[childid].size  = 0.5 * size
                    self.nodelist[childid].xc[0] = self.nodelist[nodeid].xc[0] + 0.25*size*(2*ix-1)
                    self.nodelist[childid].xc[1] = self.nodelist[nodeid].xc[1] + 0.25*size*(2*iy-1)
                    self.nodelist[childid].xc[2] = self.nodelist[nodeid].xc[2] + 0.25*size*(2*iz-1)


    #
    # Find subnode for a particle
    #
    def findsubnode(self,nodeid,particleid):
        if self.particles[particleid][0] < self.nodelist[nodeid].xc[0]:
            ix = 0
        else:
            ix = 1
        if self.particles[particleid][1] < self.nodelist[nodeid].xc[1]:
            iy = 0
        else:
            iy = 1
        if self.particles[particleid][2] < self.nodelist[nodeid].xc[2]:
            iz = 0
        else:
            iz = 1
        return ix,iy,iz


    #
    # Insert a particle into a node
    #
    def insertparticle(self,nodeid,pid):
        if self.nodelist[nodeid].particleid >= 0:
            #
            # This node already contains a particle. 
            # Name this particle ID origpid
            #
            origpid = self.nodelist[nodeid].particleid
            if origpid == pid:
                print 'ERROR: Inserting particle that is already inserted: '+str(pid)+' '+str(origpid)
                quit()
            #
            # So we must split this node into child-nodes
            #
            self.createchildren(nodeid)
            #
            # Find in which of the 2x2x2 child nodes the original particle is
            #
            ix,iy,iz  = self.findsubnode(nodeid,origpid)
            subnodeid = self.nodelist[nodeid].childrenids[ix,iy,iz]
            #
            # Insert that particle in that subnode
            #
            self.insertparticle(subnodeid,origpid)
            #
            # Find in which of the 2x2x2 child nodes the current particle is
            #
            ix,iy,iz  = self.findsubnode(nodeid,pid)
            subnodeid = self.nodelist[nodeid].childrenids[ix,iy,iz]
            #
            # Insert that particle in that subnode
            #
            self.insertparticle(subnodeid,pid)
            #
            # Now remove the particle ID from the current node
            #
            self.nodelist[nodeid].particleid = -1
        else:
            #
            # This node is either empty or has children
            #
            if self.nodelist[nodeid].leaf == 1:
                #
                # Node is empty, so fill it with the particle
                #
                self.nodelist[nodeid].particleid = pid
            else:
                #
                # Node has children, so we must figure out in which subnode it is
                #
                ix,iy,iz  = self.findsubnode(nodeid,pid)
                subnodeid = self.nodelist[nodeid].childrenids[ix,iy,iz]
                #
                # Insert the particle in that subnode
                #
                self.insertparticle(subnodeid,pid)


    #
    # Insert all particles
    #
    def insertallparticles(self):
        for pid in range(len(self.particles)):
            self.insertparticle(0,pid)


    #
    # Compute multipoles (here: masses and center of masses)
    #
    def computemultipoles(self,nodeid):
        cenm = [0.,0.,0.]
        mass = 0.
        if self.nodelist[nodeid].leaf == 1:
            #
            # No children, so either 0 or 1 particle
            #
            if self.nodelist[nodeid].particleid >= 0:
                #
                # We have a particle (all particles have mass 1 by assumption)
                #
                pid = self.nodelist[nodeid].particleid
                cenm[:] = self.particles[pid][0:3]
                mass    = 1.
            else:
                #
                # It is empty
                #
                cenm[:] = [0,0,0]
                mass  = 0.0
        else:
            #
            # Yes children, so visit all of them, and 
            # add the masses and compute the center of mass
            #
            cenm = [0.,0.,0.]
            mass = 0.
            for iz in range(0,2):
                for iy in range(0,2):
                    for ix in range(0,2):
                        id   = self.nodelist[nodeid].childrenids[ix,iy,iz]
                        cm,m = self.computemultipoles(id)
                        # ....TO BE FILLED IN....
                        print "Please replace this print statement with your own code"

        #
        # Store center of mass and mass into this node
        #
        self.nodelist[nodeid].cm[:] = cenm
        self.nodelist[nodeid].mass  = mass
        #
        # Now return center of mass and the mass
        #
        return cenm,mass


    #
    # Compute the gravity force on particle pid for node nodeid
    #
    def gforce(self,nodeid,pid,anglemax):
        #
        # Get the position of the particle (its mass is by assumption 1.)
        #
        x     = [0.,0.,0.]
        x[:]  = self.particles[pid][0:3]
        mass  = 1.0
        #
        # Get the position of the center of mass of the cell and the cell's mass
        #
        cm    = [0.,0.,0.]
        cm[:] = self.nodelist[nodeid].cm
        m     = self.nodelist[nodeid].mass
        #
        # Prepare the force array
        #
        force = np.array([0,0,0],float)
        #
        # Calculate the opening angle
        #
        r     = sqrt((cm[0]-x[0])**2+(cm[1]-x[1])**2+(cm[2]-x[2])**2)
        angle = self.nodelist[nodeid].size/(r+1e-35)
        #
        # Now make a distinction:
        #
        if angle < anglemax or self.nodelist[nodeid].leaf == 1:
            #
            # This is a small enough branch or it is a leaf.
            # In either case just use the node's cm and mass.
            # But avoid self-attraction!
            #
            # ....TO BE FILLED IN....
            print "Please replace this print statement with your own code"

        else:
            #
            # We must walk further down the tree
            #
            for iz in range(0,2):
                for iy in range(0,2):
                    for ix in range(0,2):
                        cid = self.nodelist[nodeid].childrenids[ix,iy,iz]
                        force[:] = force + self.gforce(cid,pid,anglemax)
        #
        # We now return the force we have calculated
        #
        return force


    #
    # Compute gravity force for all particles
    #
    def allgforces(self,anglemax):
        nrp = len(self.particles)
        for pid in range(nrp):
            self.forces[pid][:] = self.gforce(0,pid,anglemax)

        

