#include "sma_filter.h"
#include <string.h>

int sma_filter_init(sma_filter_t *filter, filter_data_t *data, unsigned int size)
{
    if (!filter || !data || !size) {
        return SMA_FILTER_ERROR_INVALID_PARAM;
    }

    filter->data = data;
    filter->size = size;
    filter->index = 0;
    filter->sum = 0;
    filter->count = 0;
    memset(filter->data, 0, size * sizeof(filter_data_t));

    return SMA_FILTER_ERROR_OK;
}

int sma_filter_run(sma_filter_t *filter, filter_data_t input, filter_data_t *output)
{
    if (!filter || !output) {
        return SMA_FILTER_ERROR_INVALID_PARAM;
    }

    // Add the new value to the sum
    filter->sum += input;

    // If we are at the max size, subtract the oldest value from the sum
    if (filter->count == filter->size) {
        filter->sum -= filter->data[filter->index];
    } else {
        filter->count++;
    }

    // Store the new value in the data array
    filter->data[filter->index] = input;

    // Increment the index
    filter->index = (filter->index + 1) % filter->size;

    // Calculate the average
    *output = (filter_data_t)(filter->sum / (filter_data_t)filter->count);

    return (filter->count == filter->size) ? SMA_FILTER_ERROR_OK : SMA_FILTER_ERROR_INVALID_OUTPUT;
}
