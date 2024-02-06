//MIT License
//
//Copyright (c) 2023 budgettsfrog
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
#ifndef FIXED_POINT_H_
#define FIXED_POINT_H_

// Protect against C++ compilers
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include <stdint.h>
#include <stddef.h>

#ifndef ENABLE_FLOATING_POINT_MATH
#define ENABLE_FLOATING_POINT_MATH 0
#endif /* ENABLE_FLOATING_POINT_MATH */

// Define filter data types based on floating point enabled or not
#if ENABLE_FLOATING_POINT_MATH
typedef double     filter_coeff_t;
typedef float     filter_data_t;
typedef double     filter_accum_t;
#else
typedef long long  filter_coeff_t;
typedef long   filter_data_t;
typedef long long  filter_accum_t;
#endif /* ENABLE_FLOATING_POINT_MATH */

#if ENABLE_FLOATING_POINT_MATH
#define TO_FIXED_POINT(x)   (x)
#define FROM_FIXED_POINT(x) (x)
#else
#define FIXED_POINT_FRACTIONAL_BITS ((sizeof(filter_data_t) * 8) - 1)
#define FIXED_POINT_SCALING_FACTOR  (1ULL << FIXED_POINT_FRACTIONAL_BITS)
#define TO_FIXED_POINT(x)   ((x) * FIXED_POINT_SCALING_FACTOR)
#define FROM_FIXED_POINT(x) ((x) >> FIXED_POINT_FRACTIONAL_BITS)
#endif /* ENABLE_FLOATING_POINT_MATH */

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* FIXED_POINT_H_ */