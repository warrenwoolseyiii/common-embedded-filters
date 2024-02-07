#include "../impl/sma_filter/sma_filter.h"
#include "../impl/iir_filter/iir_filter.h"
#include "../impl/iir_filter/iir_config.h"
#include "../impl/fir_filter/fir_filter.h"
#include "../impl/fir_filter/fir_config.h"
#include "../impl/fixed_point.h"

#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

// Filter configuration parameters
#define SMA_FILTER_SIZE 10

// Argument strings
#define ARG_INPUT_FILE_LONG   "--input-file"
#define ARG_INPUT_FILE_SHORT  "-i"
#define ARG_OUTPUT_FILE_LONG  "--output-file"
#define ARG_OUTPUT_FILE_SHORT "-o"
#define ARG_FILTER_TYPE_LONG  "--filter-type"
#define ARG_FILTER_TYPE_SHORT "-f"
#define ARG_SUB_FILTER_LONG   "--sub-filter"
#define ARG_SUB_FILTER_SHORT  "-s"
#define ARG_HELP_LONG         "--help"
#define ARG_HELP_SHORT        "-h"

void print_help()
{
    printf("Usage: filter_example -i <input file> -o <output file> -f <filter type> -s <sub filter type>\n");
    printf("Filter types:\n");
    printf("  sma - Simple Moving Average\n");
    printf("  iir - Infinite Impulse Response\n");
    printf("  iir-biquad - Infinite Impulse Response Biquad\n");
    printf("  fir - Finite Impulse Response\n");
    printf("Sub filter types:\n");
    printf("  highpass - High pass filter\n");
    printf("  lowpass - Low pass filter\n");
    printf("  bandpass - Band pass filter\n");
    printf("  bandstop - Band stop filter\n");
}

int main(int argc, char *argv[])
{
    // Check for help
    if (argc == 2 && (!strcmp(argv[1], ARG_HELP_LONG) || !strcmp(argv[1], ARG_HELP_SHORT))) {
        print_help();
        return 0;
    }

    // Check for correct number of arguments
    if (argc < 7) {
        printf("Incorrect number of arguments\n");
        print_help();
        return -1;
    }

    // Check that the filter type is valid
    if (strcmp(argv[6], "sma") && strcmp(argv[6], "iir") && strcmp(argv[6], "iir-biquad") && strcmp(argv[6], "fir")) {
        printf("Invalid filter type\n");
        print_help();
        return -1;
    }

    // Echo the arguments for now
    printf("Input file: %s\n", argv[2]);
    printf("Output file: %s\n", argv[4]);
    printf("Filter type: %s\n", argv[6]);
    if (argc == 9) {
        printf("Sub filter type: %s\n", argv[8]);
    }

    /*
      * We assume the following:
      * 1. Data is in .csv format
      * 2. The first column is the time stamp, and is represented as milliseconds and is an integer
      * 3. All columns after that are the data column
      * 4. We set up a filter object for each data column
      */
    // Open the input and output files
    FILE *input_file = fopen(argv[2], "r");
    FILE *output_file = fopen(argv[4], "w");

    // Check that the files opened correctly
    if (!input_file) {
        printf("Failed to open input file\n");
        return -1;
    }
    if (!output_file) {
        printf("Failed to open output file\n");
        return -1;
    }

    // Read the first line of the file, base the number of columns on the number of entries in the first line
    char line[1024];
    fgets(line, 1024, input_file);
    fprintf(output_file, "%s", line);
    int   num_columns = 0;
    char *token = strtok(line, ",");
    while (token) {
        num_columns++;
        token = strtok(NULL, ",");
    }

    // Void pointer to the filter object
    void *filter = (void *)0;

    // Print the fixed point configuration, print the size of all the filter types in bits
    printf("filter_coeff_t: %lu bits\n", sizeof(filter_coeff_t) * 8);
    printf("filter_data_t: %lu bits\n", sizeof(filter_data_t) * 8);
    printf("filter_accum_t: %lu bits\n", sizeof(filter_accum_t) * 8);

    // Create the filter object using dynamic memory and based on the filter type
    if (!strcmp(argv[6], "sma")) {
        filter = (void *)malloc(sizeof(sma_filter_t) * num_columns);

        // Now intialize the filter
        for (int i = 0; i < num_columns; i++) {
            sma_filter_init((sma_filter_t *)filter + i, (filter_data_t *)malloc(sizeof(filter_data_t) * SMA_FILTER_SIZE),
                            SMA_FILTER_SIZE);
        }
    } else if (!strcmp(argv[6], "iir")) {
        filter = (void *)malloc(sizeof(iir_filter_t) * num_columns);

        // Now intialize the filter
        for (int i = 0; i < num_columns; i++) {
            iir_filter_init((iir_filter_t *)filter + i, _iir_b_coeffs, _iir_a_coeffs,
                            (filter_accum_t *)malloc(sizeof(filter_accum_t) * IIR_NUM_COEFFS),
                            (filter_accum_t *)malloc(sizeof(filter_accum_t) * IIR_NUM_COEFFS),
                            IIR_NUM_COEFFS);
        }
    } else if (!strcmp(argv[6], "iir-biquad")) {
        filter = (void *)malloc(sizeof(iir_biquad_filter_t) * num_columns);

        // Now intialize the filter
        for (int i = 0; i < num_columns; i++) {
            iir_biquad_filter_init((iir_biquad_filter_t *)filter + i, _iir_sos_coeffs,
                                   (filter_accum_t *)malloc(sizeof(filter_accum_t) * (IIR_BIQUAD_NUM_TERMS * 4)),
                                   IIR_BIQUAD_NUM_TERMS);
        }
    } else if (!strcmp(argv[6], "fir")) {
        filter = (void *)malloc(sizeof(fir_filter_t) * num_columns);

        // Now intialize the filter
        for (int i = 0; i < num_columns; i++) {
            fir_filter_init((fir_filter_t *)filter + i, _fir_b_coeffs,
                            (filter_accum_t *)malloc(sizeof(filter_accum_t) * FIR_NUM_COEFFS), FIR_NUM_COEFFS);
        }
    } else {
        printf("Invalid filter type\n");
        print_help();
        return -1;
    }

    // Now read the rest of the file and run the filter on each column
    unsigned int delta_time = 0;
    unsigned int prev_time = 0;
    unsigned int line_count = 0;
    while (fgets(line, 1024, input_file)) {
        // Get the time stamp
        token = strtok(line, ",");
        unsigned int time_stamp = atoi(token);
        if (prev_time == 0) {
            prev_time = time_stamp;
        } else {
            delta_time += time_stamp - prev_time;
            prev_time = time_stamp;
        }

        // Write the time stamp to the output file
        fprintf(output_file, "%u,", time_stamp);

        // Get the data
        for (int i = 0; i < num_columns - 1; i++) {
            token = strtok(NULL, ",");
            filter_data_t input = (filter_data_t)atof(token);
            filter_data_t output = 0;

            // Run the filter
            if (!strcmp(argv[6], "sma")) {
                sma_filter_run((sma_filter_t *)filter + i, input, &output);
            } else if (!strcmp(argv[6], "iir")) {
                if (iir_filter_run((iir_filter_t *)filter + i, input, &output) == IIR_FILTER_ERROR_INVALID_OUTPUT) {
                    output = 0;
                }
            } else if (!strcmp(argv[6], "iir-biquad")) {
                if (iir_biquad_filter_run((iir_biquad_filter_t *)filter + i, input, &output) == IIR_FILTER_ERROR_INVALID_OUTPUT) {
                    output = 0;
                }
            } else if (!strcmp(argv[6], "fir")) {
                fir_filter_run((fir_filter_t *)filter + i, input, &output);
            }

            // Write the output to the file, if this is the last column, don't write a comma
            if (i < num_columns - 2) {
                fprintf(output_file, "%f,", (float)output);
            } else {
                fprintf(output_file, "%f", (float)output);
            }
        }

        // Write a new line
        fprintf(output_file, "\n");

        // Increment the line count
        line_count++;
    }

    // Close the files
    fclose(input_file);
    fclose(output_file);

    // Print the average time delta
    printf("Average time delta: %f ms\n", (float)delta_time / (float)line_count);
    printf("Average sample rate: %f Hz\n", 1000.0 / ((float)delta_time / (float)line_count));

    // Based on the filter size and type, free all of the sub objects
    if (!strcmp(argv[6], "sma")) {
        for (int i = 0; i < num_columns; i++) {
            free(((sma_filter_t *)filter + i)->data);
        }
    } else if (!strcmp(argv[6], "iir")) {
        for (int i = 0; i < num_columns; i++) {
            free(((iir_filter_t *)filter + i)->prev_inputs);
            free(((iir_filter_t *)filter + i)->prev_outputs);
        }
    } else if (!strcmp(argv[6], "iir-biquad")) {
        for (int i = 0; i < num_columns; i++) {
            free(((iir_biquad_filter_t *)filter + i)->delay_elements);
        }
    } else if (!strcmp(argv[6], "fir")) {
        for (int i = 0; i < num_columns; i++) {
            free(((fir_filter_t *)filter + i)->prev_inputs);
        }
    }

    // Now free the filter object
    free(filter);
}
