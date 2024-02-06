# This is a utility script that converts time stamps in the sample logs (Flume format)
# from steps to milliseconds.

import sys

if len(sys.argv) < 2:
    print("Please provide a file name as a command line argument.")
    sys.exit(1)

file_path = sys.argv[1]
out_file_path = file_path + ".out"

try:
    with open(file_path, 'r') as file:
        line_count = 0
        for line in file:
            # Skip the first line
            if line_count == 0:
                line_count += 1
                # Write the first line to the output file
                with open(out_file_path, 'w') as out_file:
                    out_file.write(line)
                continue

            # Split the line into a list of csv values, the first value is time, shift it to the right by 8 bits and create a new line
            values = line.split(',')
            time = int(values[0]) >> 8
            values[0] = str(time)
            new_line = ','.join(values)

            # Append the new line to the output file
            with open(out_file_path, 'a') as out_file:
                out_file.write(new_line)
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
