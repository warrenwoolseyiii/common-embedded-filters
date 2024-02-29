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
#ifndef IIR_FILTER_H_
#define IIR_FILTER_H_

// Protect against C++ compilers
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../filter_types.h"

#define IIR_FILTER_ERROR_OK             0
#define IIR_FILTER_ERROR_INVALID_PARAM  -1
#define IIR_FILTER_ERROR_INVALID_OUTPUT -2

/**
  * @brief IIR filter structure
  */
typedef struct
{
    unsigned int    num_coeffs;
    unsigned int    count;
    filter_coeff_t *b_coeffs;
    filter_coeff_t *a_coeffs;
    filter_accum_t *prev_inputs;
    filter_accum_t *prev_outputs;
} iir_filter_t;

/**
  * @brief IIR biquad filter structure
  */
typedef struct
{
    unsigned int num_coeffs;
    unsigned int count;
    filter_coeff_t(*sos_coeffs)[6];
    filter_accum_t(*delay_elements);
} iir_biquad_filter_t;

/**
  * @brief Initialize the filter
  * @param filter Pointer to the filter
  * @param b_coeffs Pointer to the numerator coefficients
  * @param a_coeffs Pointer to the denominator coefficients
  * @param prev_inputs Pointer to the previous inputs
  * @param prev_outputs Pointer to the previous outputs
  * @param num_coeffs The number of coefficients that need to be applied
  * @return IIR_FILTER_ERROR_OK on success, negative on error
  */
int iir_filter_init(iir_filter_t *filter, filter_coeff_t *b_coeffs, filter_coeff_t *a_coeffs, filter_accum_t *prev_inputs, filter_accum_t *prev_outputs, unsigned int num_coeffs);

/**
  * @brief Run an IIR filter on the input
  * @param filter Pointer to the filter
  * @param input Input value
  * @param output Pointer to the output value
  * @return IIR_FILTER_ERROR_OK on success, negative on error
  */
int iir_filter_run(iir_filter_t *filter, filter_data_t input, filter_data_t *output);

/**
  * @brief Initialize the biquad filter
  * @param filter Pointer to the filter
  * @param sos_coeffs Pointer to the second order section coefficients
  * @param delay_elements Pointer to the previous inputs
  * @param num_coeffs The number of coefficients that need to be applied
  */
int iir_biquad_filter_init(iir_biquad_filter_t *filter, filter_coeff_t (*sos_coeffs)[6], filter_accum_t *delay_elements, unsigned int num_coeffs);

/**
  * @brief Run a biquad filter on the input
  * @param filter Pointer to the filter
  * @param input Input value
  * @param output Pointer to the output value
  * @return IIR_FILTER_ERROR_OK on success, negative on error
  */
int iir_biquad_filter_run(iir_biquad_filter_t *filter, filter_data_t input, filter_data_t *output);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* IIR_FILTER_H_ */
