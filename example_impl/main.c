#include "../impl/sma_filter/sma_filter.h"
#include "../impl/iir_filter/iir_filter.h"

#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

// Filter configuration parameters
#define SMA_FILTER_SIZE  10
#define IIR_FILTER_ORDER 1

// Filter coefficients for iir high pass filter
filter_coeff_t _iir_a_coeffs[IIR_FILTER_ORDER + 1] = { TO_FIXED_POINT(1.00000000000000000000f), TO_FIXED_POINT(-0.99217670017750692057f) };
filter_coeff_t _iir_b_coeffs[IIR_FILTER_ORDER + 1] = { TO_FIXED_POINT(0.99608835008875340478f), TO_FIXED_POINT(-0.99608835008875340478f) };

// Argument strings
#define ARG_INPUT_FILE_LONG   "--input-file"
#define ARG_INPUT_FILE_SHORT  "-i"
#define ARG_OUTPUT_FILE_LONG  "--output-file"
#define ARG_OUTPUT_FILE_SHORT "-o"
#define ARG_FILTER_TYPE_LONG  "--filter-type"
#define ARG_FILTER_TYPE_SHORT "-f"
#define ARG_HELP_LONG         "--help"
#define ARG_HELP_SHORT        "-h"

void print_help()
{
    printf("Usage: filter_example -i <input file> -o <output file> -f <filter type>\n");
    printf("Filter types:\n");
    printf("  sma - Simple Moving Average\n");
    printf("  iir - Infinite Impulse Response\n");
}

int main(int argc, char *argv[])
{
    // Check for help
    if (argc == 2 && (!strcmp(argv[1], ARG_HELP_LONG) || !strcmp(argv[1], ARG_HELP_SHORT))) {
        print_help();
        return 0;
    }

    // Check for correct number of arguments
    if (argc != 7) {
        printf("Incorrect number of arguments\n");
        print_help();
        return -1;
    }

    // Check that the filter type is valid
    if (strcmp(argv[6], "sma") && strcmp(argv[6], "iir")) {
        printf("Invalid filter type\n");
        print_help();
        return -1;
    }

    // Echo the arguments for now
    printf("Input file: %s\n", argv[2]);
    printf("Output file: %s\n", argv[4]);
    printf("Filter type: %s\n", argv[6]);

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

    // Create the filter object using dynamic memory and based on the filter type
    if (!strcmp(argv[6], "sma")) {
        filter = (void *)malloc(sizeof(sma_filter_t) * num_columns);

        // Now intialize the filter
        for (int i = 0; i < num_columns; i++) {
            sma_filter_init((sma_filter_t *)filter + i, (filter_data_t *)malloc(sizeof(filter_data_t) * SMA_FILTER_SIZE), SMA_FILTER_SIZE);
        }
    } else if (!strcmp(argv[6], "iir")) {
        filter = (void *)malloc(sizeof(iir_filter_t) * num_columns);

        // Now intialize the filter
        for (int i = 0; i < num_columns; i++) {
            iir_filter_init((iir_filter_t *)filter + i, _iir_b_coeffs, _iir_a_coeffs, (filter_data_t *)malloc(sizeof(filter_data_t) * IIR_FILTER_ORDER), (filter_data_t *)malloc(sizeof(filter_data_t) * IIR_FILTER_ORDER), IIR_FILTER_ORDER);
        }
    } else {
        printf("Invalid filter type\n");
        print_help();
        return -1;
    }

    // Now read the rest of the file and run the filter on each column
    while (fgets(line, 1024, input_file)) {
        // Get the time stamp
        token = strtok(line, ",");
        unsigned int time_stamp = atoi(token);

        // Write the time stamp to the output file
        fprintf(output_file, "%u,", time_stamp);

        // Get the data
        for (int i = 0; i < num_columns - 1; i++) {
            token = strtok(NULL, ",");
            filter_data_t input = (filter_data_t)atof(token);
            filter_data_t output = input; //0;

            // Run the filter
            if (!strcmp(argv[6], "sma")) {
                sma_filter_run((sma_filter_t *)filter + i, input, &output);
            } else if (!strcmp(argv[6], "iir")) {
                iir_high_pass_filter_run((iir_filter_t *)filter + i, input, &output);
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
    }

    // Close the files
    fclose(input_file);
    fclose(output_file);

    // Based on the filter size and type, free all of the sub objects
    if (!strcmp(argv[6], "sma")) {
        for (int i = 0; i < num_columns; i++) {
            free(((sma_filter_t *)filter + i)->data);
        }
    } else if (!strcmp(argv[6], "iir")) {
        for (int i = 0; i < num_columns; i++) {
            free(((iir_filter_t *)filter + i)->b_coeffs);
            free(((iir_filter_t *)filter + i)->a_coeffs);
            free(((iir_filter_t *)filter + i)->prev_inputs);
            free(((iir_filter_t *)filter + i)->prev_outputs);
        }
    }

    // Now free the filter object
    free(filter);
}
