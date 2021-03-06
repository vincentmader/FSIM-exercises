/* CAUTION: This is the combined ANSI and traditional K&R C version
   of the Numerical Recipes utility file complex.h.  Do not confuse
   this file with the same-named file complex.h that is supplied in
   the 'include' subdirectory.  *That* file contains only ANSI.
   *This* file contains both ANSI and traditional K&R versions,
   along with #ifdef macros to select the correct version.                */

#ifndef _NR_COMPLEX_H_
#define _NR_COMPLEX_H_

#ifndef _FCOMPLEX_DECLARE_T_
typedef struct FCOMPLEX {float r,i;} fcomplex;
#define _FCOMPLEX_DECLARE_T_
#endif /* _FCOMPLEX_DECLARE_T_ */

#if defined(__STDC__) || defined(ANSI) || defined(NRANSI) /* ANSI */

fcomplex Cadd(fcomplex a, fcomplex b);
fcomplex Csub(fcomplex a, fcomplex b);
fcomplex Cmul(fcomplex a, fcomplex b);
fcomplex Complex(float re, float im);
fcomplex Conjg(fcomplex z);
fcomplex Cdiv(fcomplex a, fcomplex b);
float Cabs(fcomplex z);
fcomplex Csqrt(fcomplex z);
fcomplex RCmul(float x, fcomplex a);

#else /* ANSI */
/* traditional - K&R */

fcomplex Cadd();
fcomplex Csub();
fcomplex Cmul();
fcomplex Complex();
fcomplex Conjg();
fcomplex Cdiv();
float Cabs();
fcomplex Csqrt();
fcomplex RCmul();

#endif /* ANSI */

#endif /* _NR_COMPLEX_H_ */
