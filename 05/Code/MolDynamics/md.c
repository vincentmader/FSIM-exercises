/*************************************/
/* NVT ensemble with neighbours list */
/*************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <math.h>
#include <time.h>
#define MAXPART 10000

// this is our data type for storing the information for the particles
typedef struct {
  double pos[3];
  double vel[3];
  double acc[3];
  double acc_prev[3];
  double pot;
  int n_neighbors; // length of neighbor list
  int neighbors[MAXPART]; // neighbors (with index larger than current particle)
} particle;

// auxiliary function to create a Gaussian random deviate
double gaussian_rnd(void) {
  // ---students ---
  int r_1, r_2, n_max= 32767;
  time_t t;
  double ;
   /* Intializes random number generator */
   srand((unsigned) time(&t));
  r_1 = rand(n);
  r_2 = rand(n);

      double x, ret;
   x = 2.7;

   /* finding log(2.7) */
   ret = log(x);
   printf("log(%lf) = %lf", x, ret);

   double sqrt(double x)



  // --- end ---
}

// This function initializes our particle set.
void initialize(particle *p, double L, int N1d, double sigma_v) {
  int n = 0;

  double dl = L / N1d;

  for(int i = 0; i < N1d; i++) {
    for(int j = 0; j < N1d; j++) {
      for(int k = 0; k < N1d; k++) {
        // --- students ---
        p[n].pos[0] = ;
        p[n].pos[1] = ;
        p[n].pos[2] = ;

        p[n].vel[0] = ;
        p[n].vel[1] = ;
        p[n].vel[2] = ;

        // --- end ---
        n++;
      }
    }
  }
}

// This function updates the velocities by applying the accelerations for the given time interval.
void kick(particle * p, int ntot, double dt) {
  // --- students ---

  // --- end ---
}

// This function drifts the particles with their velocities for the given time interval.
// Afterwards, the particles are mapped periodically back to the box if needed.
void drift(particle * p, int ntot, double boxsize, double dt) {
  // --- students ---

  // --- end ---
}

// This function calculates the potentials and forces for all particles. For simplicity,
// we do this by going through all particle pairs i-j, and then adding the contributions both to i and j.
void calc_forces(particle * p, int ntot, double boxsize, double rcut)
{
  int n;
  double rcut2 = rcut * rcut;
  double r2, r, r6, r12, dr[3], acc[3], pot;

  // first, set all the accelerations and potentials to zero
  for (int i = 0; i < ntot; i++) {
    p[i].pot = 0;
    for (int k = 0; k < 3; k++) {
      p[i].acc[k] = 0;
    }
  }

  // sum over all distinct pairs
  for (int i = 0; i < ntot; i++) {
    for (n = 0; n < p[i].n_neighbors; n++) {
      int j = p[i].neighbors[n];

      // Calculate squared distance
      double r2 = 0;
      for (int k = 0; k < 3; k++) {
        dr[k] = p[i].pos[k] - p[j].pos[k];

        // Ensure we find the shortest distance bewteen particles
        if (dr[k] > 0.5 * boxsize) {
          dr[k] -= boxsize;
        }

        if (dr[k] < -0.5 * boxsize) {
          dr[k] += boxsize;
        }

        r2 += dr[k] * dr[k];
      }

      // --- students ---

      if (r2 < rcut2) {
        r = sqrt(r2);
        r6 = r2 * r2 * r2;
        r12 = r6 * r6;

        // now calculate the Lennard-Jones potential for the pair
        pot = ;
        p[i].pot += pot;
        p[j].pot += pot;

        // now calculate the Lennard-Jones force between the particles
        for (int k = 0; k < 3; k++) {
          acc[k] = ;
          p[i].acc[k] += acc[k];
          p[j].acc[k] -= acc[k];
        }
      }

      // --- end ---
    }
  }
}

// This function calculates the total kinetic and total potential energy, averaged per particle.
void calc_energies(particle *p, int ntot, double *ekin, double *epot) {
  double sum_pot = 0, sum_kin = 0;

  for (int i = 0; i < ntot; i++) {
    sum_pot += p[i].pot;

    // --- students ---

    for(int k = 0; k < 3; k++) {
      sum_kin += ;
    }
  }

  // --- end ---

  *ekin = 0.5 * sum_kin / ntot;
  *epot = 0.5 * sum_pot / ntot;
}



/*
* main driver routine
*/
int main(int argc, char **argv) {
  // Input parameters
  double target_temperature = 120.0; // target temperature
  double sig_v = sqrt(target_temperature / 120.0);
  int N1d = 5; // particles per dimension
  int N = N1d * N1d * N1d; // total particle number

  // Box parameters
  double L = 10.0 * N1d;
  double rcut = L;
  double boxsize = L;

  // Time control
  int output_frequency = 10;
  int nsteps = 1000; // number of steps to take
  double dt = 0.01; // timestep size


  double ekin, epot;
  double r;

  // allocate storage for our particles
  particle *p = malloc(N * sizeof(particle));

  // let's initialize the particles
  initialize(p, L, N1d, sig_v);

  // calculate the forces at t=0
  calc_forces(p, N, boxsize, rcut);

  // create an output file
  char fname[100];

  sprintf(fname, "output_T%d.txt", (int)target_temperature);

  FILE *fd = fopen(fname, "w");

  // measure energies at beginning, and output this to the file and screen
  calc_energies(p, N, &ekin, &epot);
  fprintf(fd, "%6d %10g %10g %10.8g\n", 0, ekin, epot, ekin + epot);

  printf("nsteps: %d, T: %f \n", nsteps, target_temperature);


  // --- students ---

  // Carry out the time integration using leapfrog integration
  clock_t tic = clock();
  for (int step = 0; step < nsteps; step++) {

  }

  // --- end ---
  printf("boxsize = %20.6f\n", boxsize);

  fclose(fd);
  return 0;
}
