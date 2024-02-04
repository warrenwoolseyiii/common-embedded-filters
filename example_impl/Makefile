# Compiler and compiler flags
CC = gcc
CFLAGS = -Wall -g

# Executable name
TARGET = filter_example

# Object files
OBJS = sma_filter.o iir_filter.o iir_coefficients.o main.o

# Default target
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Object file rules
main.o: ../impl/sma_filter/sma_filter.c ../impl/iir_filter/iir_filter.c
	$(CC) $(CFLAGS) -c main.c

sma_filter.o: ../impl/sma_filter/sma_filter.c ../impl/sma_filter/sma_filter.h
	$(CC) $(CFLAGS) -c ../impl/sma_filter/sma_filter.c

iir_filter.o: ../impl/iir_filter/iir_filter.c ../impl/iir_filter/iir_filter.h
	$(CC) $(CFLAGS) -c ../impl/iir_filter/iir_filter.c

iir_coefficients.o: ../impl/iir_filter/iir_coefficients.c ../impl/iir_filter/iir_config.h
	$(CC) $(CFLAGS) -c ../impl/iir_filter/iir_coefficients.c

# Clean target
clean:
	rm -f $(TARGET) $(OBJS)
