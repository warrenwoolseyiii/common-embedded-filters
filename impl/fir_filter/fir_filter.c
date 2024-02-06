#include "fir_filter.h"
#include <string.h>

int fir_filter_init(fir_filter_t *filter, filter_coeff_t *b_coeffs, filter_accum_t *prev_inputs, unsigned int num_coeffs)
{
    if (!filter || !b_coeffs || !prev_inputs || num_coeffs == 0) {
        return FIR_FILTER_ERROR_INVALID_PARAM;
    }

    filter->b_coeffs = b_coeffs;
    filter->prev_inputs = prev_inputs;
    filter->num_coeffs = num_coeffs;
    filter->count = 0;
    memset(filter->prev_inputs, 0, sizeof(filter_accum_t) * num_coeffs);

    return FIR_FILTER_ERROR_OK;
}

int fir_filter_run(fir_filter_t *filter, filter_data_t input, filter_data_t *output)
{
    if (!filter || !output) {
        return FIR_FILTER_ERROR_INVALID_PARAM;
    }

    filter_accum_t in = (filter_accum_t)input;
    filter_accum_t new_output = FROM_FIXED_POINT(filter->b_coeffs[0] * in);
    for (int i = 1; i < filter->num_coeffs; i++)
    {
        new_output += FROM_FIXED_POINT(filter->b_coeffs[i] * filter->prev_inputs[i - 1]);
    }

    // Shift the buffer contents
    for (int i = filter->num_coeffs - 1; i > 0; i--)
    {
        filter->prev_inputs[i] = filter->prev_inputs[i - 1];
    }
    filter->prev_inputs[0] = in;

    // Assign the calculated output
    *output = (filter_data_t)new_output;

    return FIR_FILTER_ERROR_OK;
}
