#ifndef FILTER_TYPES_H_
#define FILTER_TYPES_H_

#include <stdint.h>
#include <stddef.h>
//#include <stdfix.h>

// Uncomment this if you want to use floating point math instead of fixed point
// #define FILTER_USE_FP_MATH

#if defined(FILTER_USE_FP_MATH)
typedef double        filter_coeff_t;
typedef float         filter_data_t;
typedef double        filter_accum_t;
#else
typedef long _Accum   filter_coeff_t;
typedef _Accum        filter_data_t;
typedef long _Accum   filter_accum_t;
#endif /* FILTER_USE_FP_MATH */

#endif /* FILTER_TYPES_H_ */
