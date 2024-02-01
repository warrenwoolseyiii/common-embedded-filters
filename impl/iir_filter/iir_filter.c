#include "iir_filter.h"
#include <string.h>

int iir_filter_init(iir_filter_t *filter, filter_coeff_t *b_coeffs, filter_coeff_t *a_coeffs, filter_accum_t *prev_inputs, filter_accum_t *prev_outputs, unsigned int filter_order)
{
    if (!filter || !b_coeffs || !a_coeffs || !prev_inputs || !prev_outputs || filter_order == 0) {
        return IIR_FILTER_ERROR_INVALID_PARAM;
    }

    filter->b_coeffs = b_coeffs;
    filter->a_coeffs = a_coeffs;
    filter->prev_inputs = prev_inputs;
    filter->prev_outputs = prev_outputs;
    filter->filter_order = filter_order;
    filter->count = 0;
    memset(filter->prev_inputs, 0, sizeof(filter_accum_t) * filter_order);
    memset(filter->prev_outputs, 0, sizeof(filter_accum_t) * filter_order);

    return IIR_FILTER_ERROR_OK;
}

int iir_high_pass_filter_run(iir_filter_t *filter, filter_data_t input, filter_data_t *output)
{
    if (!filter || !output) {
        return IIR_FILTER_ERROR_INVALID_PARAM;
    }

    filter_accum_t in = (filter_accum_t)input;
    filter_accum_t new_output = FROM_FIXED_POINT(filter->b_coeffs[0] * in);
    for (int i = 1; i <= filter->filter_order; i++)
    {
        new_output += FROM_FIXED_POINT(filter->b_coeffs[i] * filter->prev_inputs[i - 1]) - FROM_FIXED_POINT(filter->a_coeffs[i] * filter->prev_outputs[i - 1]);
    }

    // Shift the buffer contents
    for (int i = filter->filter_order - 1; i > 0; i--)
    {
        filter->prev_inputs[i] = filter->prev_inputs[i - 1];
        filter->prev_outputs[i] = filter->prev_outputs[i - 1];
    }
    filter->prev_inputs[0] = in;
    filter->prev_outputs[0] = new_output;

    // Assign the calculated output
    *output = (filter_data_t)new_output;

    // Increment the state up to the filter order
    if (filter->count < filter->filter_order) {
        filter->count++;
        return IIR_FILTER_ERROR_INVALID_OUTPUT;
    }

    return IIR_FILTER_ERROR_OK;
}

int iir_low_pass_filter_run(iir_filter_t *filter, filter_data_t input, filter_data_t *output)
{
    // TODO: Implement low pass filter
    return IIR_FILTER_ERROR_INVALID_OUTPUT;
}

int iir_band_pass_filter_run(iir_filter_t *filter, filter_data_t input, filter_data_t *output)
{
    // TODO: Implement band pass filter
    return IIR_FILTER_ERROR_INVALID_OUTPUT;
}

int iir_band_stop_filter_run(iir_filter_t *filter, filter_data_t input, filter_data_t *output)
{
    // TODO: Implement band stop filter
    return IIR_FILTER_ERROR_INVALID_OUTPUT;
}
