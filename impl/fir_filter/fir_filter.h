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
#ifndef FIR_FILTER_H_
#define FIR_FILTER_H_

// Protect against C++ compilers
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../fixed_point.h"

#define FIR_FILTER_ERROR_OK             0
#define FIR_FILTER_ERROR_INVALID_PARAM  -1
#define FIR_FILTER_ERROR_INVALID_OUTPUT -2

/**
  * @brief IIR filter structure
  */
typedef struct
{
    unsigned int    num_coeffs;
    unsigned int    count;
    filter_coeff_t *b_coeffs;
    filter_accum_t *prev_inputs;
} fir_filter_t;

/**
  * @brief Initialize the filter
  * @param filter Pointer to the filter
  * @param b_coeffs Pointer to the numerator coefficients
  * @param prev_inputs Pointer to the previous inputs
  * @param num_coeffs The number of coefficients that need to be applied
  * @return FIR_FILTER_ERROR_OK on success, negative on error
  */
int fir_filter_init(fir_filter_t *filter, filter_coeff_t *b_coeffs, filter_accum_t *prev_inputs, unsigned int num_coeffs);

/**
  * @brief Run an FIR filter on the input value
  * @param filter Pointer to the filter
  * @param input Input value
  * @param output Pointer to the output value
  * @return FIR_FILTER_ERROR_OK on success, negative on error
  */
int fir_filter_run(fir_filter_t *filter, filter_data_t input, filter_data_t *output);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* FIR_FILTER_H_ */
