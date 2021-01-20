import numpy
from matplotlib.pyplot import *
import math
import time


#global parameters
pi = math.pi
i_x = 0
i_y = 1
i_z = 2
i_u = 3
i_v = 4
i_w = 5



def rand_gauss():

           #---students---#



           #---end---#

def dx_vec(i,p):

          dx = p.coord[i,i_x]-p.coord[:,i_x]
          dy = p.coord[i,i_y]-p.coord[:,i_y]
          dz = p.coord[i,i_z]-p.coord[:,i_z]

          kx1 = numpy.where((numpy.abs(dx)>(p.L/2.)) & (dx<0.))
          kx2 = numpy.where((numpy.abs(dx)>(p.L/2.)) & (dx>0.))

          ky1 = numpy.where((numpy.abs(dy)>(p.L/2.)) & (dy<0.))
          ky2 = numpy.where((numpy.abs(dy)>(p.L/2.)) & (dy>0.))

          kz1 = numpy.where((numpy.abs(dz)>(p.L/2.)) & (dz<0.))
          kz2 = numpy.where((numpy.abs(dz)>(p.L/2.)) & (dz>0.))

          dx[kx1] = p.L + dx[kx1] 
          dx[kx2] = dx[kx2] - p.L

          dy[ky1] = L + dy[ky1] 
          dy[ky2] = dy[ky2] - p.L

          dz[kz1] = L + dz[kz1] 
          dz[kz2] = dz[kz2] - p.L

          return dx,dy,dz
               



class particles:


     def __init__(self,L,N1d,sig_v,r_cut,output_frequency):

            self.N = N1d**3

            self.coord =  numpy.zeros((self.N,3))
            self.vel   =  numpy.zeros((self.N,3))

            dl = L/N1d
            
            ip = 0


            for i in range(N1d):
                for j in range(N1d):
                      for k in range(N1d):

                               #---students---#

                               self.coord[ip,i_x] = 
                               self.coord[ip,i_y] = 
                               self.coord[ip,i_z] =  
                               self.vel[ip,i_x]   =  
                               self.vel[ip,i_y]   =  
                               self.vel[ip,i_z]   =  
                               ip+=1
                               
                               #---end---#
 

            self.F     =  numpy.zeros((self.N,3))
            self.a     =  numpy.zeros((self.N,3))
            self.R     =  numpy.zeros((self.N,6)) 

            self.time         = 0.
            self.dt           = 0.01
            self.L            = L
            self.r_cut        = r_cut
            self.model_number = 0
            self.noutput      = 0
            self.E0           = 0.




            self.output_frequency = output_frequency
            self.max_output       = 300



     def get_acceleration(self):

            self.V = 0.
            self.rmin = 1e+9

            for i in range(self.N):


                      dx,dy,dz = dx_vec(i,self)
 
                      #---students---#

                      r2 = (dx**2+dy**2+dz**2)
                      self.F[:,:] = 0.0
                      k_int = (r2>0.) & (r2<self.r_cut**2)
                      r     = r2[k_int]**0.5

                      self.F[k_int,i_x] =  
                      self.F[k_int,i_y] =  
                      self.F[k_int,i_z] =  

                      self.a[i,:] = numpy.sum(self.F,axis=0)

                      V = 
                      self.V += 

                      #---end---#




     def evolve_coords(self):

   
              kx1 = numpy.where((self.coord[:,i_x]+self.R[:,i_x])>self.L)
              kx2 = numpy.where((self.coord[:,i_x]+self.R[:,i_x])<0.)
              ky1 = numpy.where((self.coord[:,i_y]+self.R[:,i_y])>self.L)
              ky2 = numpy.where((self.coord[:,i_y]+self.R[:,i_y])<0.)
              kz1 = numpy.where((self.coord[:,i_z]+self.R[:,i_z])>self.L)
              kz2 = numpy.where((self.coord[:,i_z]+self.R[:,i_z])<0.)

              kx = numpy.where(((self.coord[:,i_x]+self.R[:,i_x])>0.) & ((self.coord[:,i_x]+self.R[:,i_x])<self.L))
              ky = numpy.where(((self.coord[:,i_y]+self.R[:,i_y])>0.) & ((self.coord[:,i_y]+self.R[:,i_y])<self.L))
              kz = numpy.where(((self.coord[:,i_z]+self.R[:,i_z])>0.) & ((self.coord[:,i_z]+self.R[:,i_z])<self.L))

              self.coord[kx1,i_x] = self.coord[kx1,i_x] + self.R[kx1,i_x] - self.L
              self.coord[ky1,i_y] = self.coord[ky1,i_y] + self.R[ky1,i_y] - self.L
              self.coord[kz1,i_z] = self.coord[kz1,i_z] + self.R[kz1,i_z] - self.L

              self.coord[kx2,i_x] = self.L + self.R[kx2,i_x] - self.coord[kx2,i_x]
              self.coord[ky2,i_y] = self.L + self.R[ky2,i_y] - self.coord[ky2,i_y] 
              self.coord[kz2,i_z] = self.L + self.R[kz2,i_z] - self.coord[kz2,i_z] 

              self.coord[kx,i_x] +=  self.R[kx,i_x] 
              self.coord[ky,i_y] +=  self.R[ky,i_y]  
              self.coord[kz,i_z] +=  self.R[kz,i_z]  
   




             

     def do_leapfrog(self):


             #---students---#
            


             #---end---#
              

     def getK(self):

              #---students---#

              self.K = 

              #---end---#

     def getE(self):


              self.getK()

              #---students---#

               self.E = 

              #---end---#
             
             
              if self.model_number == 0:
                  self.E0 = self.E


     def check_for_store(self):
        
              if (self.model_number%self.output_frequency==0):

                      self.store()
                  
                      
     def store(self):
             
              numpy.savez('%d.npz'%(self.noutput),coord=self.coord,vel=self.vel,K=self.K,V=self.V,E=self.E,t=self.time,Np=self.N)

              self.noutput += 1
 
              if self.noutput >= self.max_output:
                     self.output_frequency = 20000000000

     def print_info(self):

              print('| model number=%d | (E-E0)/E0: %.7e |'%(self.model_number,(self.E-self.E0)/self.E0))


   

#//////////////////////////////////////////////////////////////////////

#input parameters

#---students---#
T                = 
sig_v            = 
N1d              = 
L                = 
r_cut            = 
output_frequency = 


Niter            = 
dt               = 

#---end---#

#main program 
t1 = time.time()

p = particles(L,N1d,sig_v,r_cut,output_frequency)
p.dt = dt


#you have to complete the program to get the energy for every step and initialize the acceleration for the leapfrog

#---students---#




for tt in range(Niter):

    p.print_info()
    p.check_for_store()
    p.do_leapfrog()
    p.model_number+=1
    p.time += p.dt

t2 = time.time()
print(t2-t1)


#---end---#

#//////////////////////////////////////////////////////////////////////

