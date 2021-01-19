import numpy as np

class NodeClass:
    def __init__(self):
        self.leaf = 1
        self.childrenids = np.zeros((2,2,2),dtype=int)
        self.xc = np.array([0.,0.,0.])
        self.size = 0.
        self.cm = np.array([0.,0.,0.])
        self.mass = 0.0
        self.particleid = -1

class TreeClass:
    def __init__(self,particles):
        self.nodelist = []
        self.nodelist.append(NodeClass())
        self.particles = particles
        self.forces = np.zeros((len(particles),3),dtype=float)
        self.interactions = np.zeros(len(particles))    #here we make a list of interactions per particle
        if len(self.particles) > 0:
            min  = np.amin(self.particles)
            max  = np.amax(self.particles)
            self.nodelist[0].size = (max-min)*1.1
            for coord in [0,1,2]:
                self.nodelist[0].xc[coord] = 0.5 * (min+max)

    def createnode(self):
        nodeid = len(self.nodelist)
        self.nodelist.append(NodeClass())
        return nodeid

    def createchildren(self,nodeid):
        if self.nodelist[nodeid].leaf == 0:
            print("ERROR: Node already has children")
            quit()
        self.nodelist[nodeid].leaf = 0
        for iz in range(0,2):
            for iy in range(0,2):
                for ix in range(0,2):
                    childid = self.createnode()
                    self.nodelist[nodeid].childrenids[ix,iy,iz] = childid
                    size = self.nodelist[nodeid].size
                    self.nodelist[childid].size  = 0.5 * size
                    self.nodelist[childid].xc[0] = self.nodelist[nodeid].xc[0] + 0.25*size*(2*ix-1)
                    self.nodelist[childid].xc[1] = self.nodelist[nodeid].xc[1] + 0.25*size*(2*iy-1)
                    self.nodelist[childid].xc[2] = self.nodelist[nodeid].xc[2] + 0.25*size*(2*iz-1)

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

    def insertparticle(self,nodeid,pid):
        if self.nodelist[nodeid].particleid >= 0:
            origpid = self.nodelist[nodeid].particleid
            if origpid == pid:
                print('ERROR: Inserting particle that is already inserted: '+str(pid)+' '+str(origpid))
                quit()
            self.createchildren(nodeid)
            ix,iy,iz  = self.findsubnode(nodeid,origpid)
            subnodeid = self.nodelist[nodeid].childrenids[ix,iy,iz]
            self.insertparticle(subnodeid,origpid)
            ix,iy,iz  = self.findsubnode(nodeid,pid)
            subnodeid = self.nodelist[nodeid].childrenids[ix,iy,iz]
            self.insertparticle(subnodeid,pid)
            self.nodelist[nodeid].particleid = -1
        else:
            if self.nodelist[nodeid].leaf == 1:
                self.nodelist[nodeid].particleid = pid
            else:
                ix,iy,iz  = self.findsubnode(nodeid,pid)
                subnodeid = self.nodelist[nodeid].childrenids[ix,iy,iz]
                self.insertparticle(subnodeid,pid)

    def insertallparticles(self):
        for pid in range(len(self.particles)):
            self.insertparticle(0,pid)


    def computemultipoles(self,nodeid):
        cenm = np.array([0.,0.,0.])
        mass = 0.
        if self.nodelist[nodeid].leaf == 1:
            if self.nodelist[nodeid].particleid >= 0:
                pid = self.nodelist[nodeid].particleid
                cenm = self.particles[pid]
                mass    = 1.
            else:
                cenm = np.array([0,0,0])
                mass  = 0.0
        else:
            for iz in range(0,2):
                for iy in range(0,2):
                    for ix in range(0,2):
                        id   = self.nodelist[nodeid].childrenids[ix,iy,iz]
                        cm,m = self.computemultipoles(id)
                        # ....TO BE FILLED IN....
                        mass += m
                        cenm += m*cm
            cenm /= mass

        self.nodelist[nodeid].cm = cenm
        self.nodelist[nodeid].mass  = mass

        return cenm,mass


    def gforce(self,nodeid,pid,anglemax):
        x     = np.array([0.,0.,0.])
        x     = self.particles[pid]

        cm    = self.nodelist[nodeid].cm
        m     = self.nodelist[nodeid].mass

        force = np.array([0,0,0],float)
        r     = np.linalg.norm(cm-x)
        if r == 0:  #avoid self-attraction
            return 0
        angle = self.nodelist[nodeid].size/(r+1e-35)
        if angle < anglemax or self.nodelist[nodeid].leaf == 1:
            #
            # This is a small enough branch or it is a leaf.
            # In either case just use the node's cm and mass.
            # But avoid self-attraction!
            #
            # ....TO BE FILLED IN....
            force = -m/r**3 * (cm-x)    #equivalent to last sheet

        else:
            self.interactions[pid] += 8 #factor 8 because 8 subnotes get called each time.
            for iz in range(0,2):
                for iy in range(0,2):
                    for ix in range(0,2):
                        cid = self.nodelist[nodeid].childrenids[ix,iy,iz]
                        force += self.gforce(cid,pid,anglemax)

        return force

    def allgforces(self,anglemax):
        nrp = len(self.particles)
        for pid in range(nrp):
            self.forces[pid] = self.gforce(0,pid,anglemax)
