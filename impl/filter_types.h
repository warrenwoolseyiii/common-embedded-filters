//MIT License
//
//Copyright (c) 2024 budgettsfrog
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
//The above copyright notice and this permission notice shall be included in all
//copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//SOFTWARE.

#ifndef FILTER_TYPES_H_
#define FILTER_TYPES_H_

#include <stdint.h>
#include <stddef.h>

// Define FILTER_USE_FLOAT_MATH at compile time to utilize floating point math.
// Define FILTER_USE_FIXED_LIB at compile time to utilize a builtin fixed point math library.
#if defined(FILTER_USE_FLOAT_MATH)
#undef FILTER_USE_FIXED_LIB
typedef double        filter_coeff_t;
typedef float         filter_data_t;
typedef double        filter_accum_t;
#elif defined(FILTER_USE_FIXED_LIB)
typedef long _Accum   filter_coeff_t;
typedef _Accum        filter_data_t;
typedef long _Accum   filter_accum_t;
#else
#warning "No fractional math defined, this could result in incorrect coefficients being generated."
typedef long        filter_coeff_t;
typedef int         filter_data_t;
typedef long        filter_accum_t;
#endif /* FILTER_USE_FP_MATH */

#endif /* FILTER_TYPES_H_ */
