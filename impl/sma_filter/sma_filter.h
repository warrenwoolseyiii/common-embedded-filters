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
#ifndef SMA_FILTER_H_
#define SMA_FILTER_H_

// Protect against C++ compilers
#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include "../fixed_point.h"

#define SMA_FILTER_ERROR_OK             0
#define SMA_FILTER_ERROR_INVALID_PARAM  -1
#define SMA_FILTER_ERROR_INVALID_OUTPUT -2

/**
  * @brief SMA filter structure
  */
typedef struct
{
    filter_data_t *data;
    unsigned int   size;
    unsigned int   index;
    filter_accum_t sum;
    unsigned int   count;
} sma_filter_t;

/**
  * @brief Initialize the filter
  * @param filter Pointer to the filter
  * @param data Pointer to the data array
  * @param size Size of the data array
  * @return SMA_FILTER_ERROR_OK if success, otherwise an error code
  */
int sma_filter_init(sma_filter_t *filter, filter_data_t *data, unsigned int size);

/**
  * @brief Run the filter on the input
  * @param filter Pointer to the filter
  * @param input Input value
  * @param output Pointer to the output value
  * @return SMA_FILTER_ERROR_OK if success, otherwise an error code
  */
int sma_filter_run(sma_filter_t *filter, filter_data_t input, filter_data_t *output);

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* SMA_FILTER_H_ */
