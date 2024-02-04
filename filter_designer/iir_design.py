import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import iirfilter, freqz, sosfreqz, sosfilt, lfilter
import argparse
import os

"""write_iir_coeffs - Write the IIR filter coefficients to a file, using both SOS and BA formats
@param sos - The second order sections
@param b - The numerator coefficients
@param a - The denominator coefficients
@param fname - The file name to write to
@return None"""
def write_iir_coeffs(sos, b, a, fname):
    try:
        with open(fname, 'w') as f:
            f.write("// This is an auto generated file by iir_design.py\n")
            f.write("// You can modify this manually or regenerate it by running iir_design.py\n")
            f.write("// See the README for more information\n")
            f.write("#include \"iir_config.h\"\n")
            f.write("filter_coeff_t _iir_b_coeffs[IIR_FILTER_ORDER + 1] = {\n")
            for i in range(len(b)):
                f.write(f"\tTO_FIXED_POINT({b[i]}),\n")
            f.write("};\n")
            f.write("filter_coeff_t _iir_a_coeffs[IIR_FILTER_ORDER + 1] = {\n")
            for i in range(len(a)):
                f.write(f"\tTO_FIXED_POINT({a[i]}),\n")
            f.write("};\n")
            f.write("filter_coeff_t _iir_sos_coeffs[IIR_BIQUAD_NUM_TERMS][6] = {\n")
            for i in range(len(sos)):
                f.write("{")
                for j in range(len(sos[i])):
                    f.write(f"TO_FIXED_POINT({sos[i][j]}),")
                f.write("},\n")
            f.write("};\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

"""write_iir_config - Write the IIR filter configuration to a file
@param num_terms - The number of terms in the biquad filter
@param filter_order - The filter order
@param start_freq - The start frequency
@param stop_freq - The stop frequency
@param fname - The file name to write to"""
def write_iir_config(num_terms, filter_order, start_freq, stop_freq, fname):
    try:
        if stop_freq is None:
            stop_freq = 0
        else:
            filter_order = filter_order * 2
        with open(fname, 'w') as f:
            f.write("// This is an auto generated file by iir_design.py\n")
            f.write("// You can modify this manually or regenerate it by running iir_design.py\n")
            f.write("// See the README for more information\n")
            f.write("#ifndef IIR_CONFIG_H_\n")
            f.write("#define IIR_CONFIG_H_\n")
            f.write("#include \"../fixed_point.h\"\n")
            f.write(f"#define IIR_BIQUAD_NUM_TERMS {num_terms}\n")
            f.write(f"#define IIR_FILTER_ORDER {filter_order}\n")
            f.write(f"#define IIR_START_FREQ {start_freq}\n")
            f.write(f"#define IIR_STOP_FREQ {stop_freq}\n")
            f.write(f"extern filter_coeff_t _iir_sos_coeffs[IIR_BIQUAD_NUM_TERMS][6];\n")
            f.write(f"extern filter_coeff_t _iir_b_coeffs[IIR_FILTER_ORDER + 1];\n")
            f.write(f"extern filter_coeff_t _iir_a_coeffs[IIR_FILTER_ORDER + 1];\n")
            f.write("#endif")
    except Exception as e:
        print(f"Error writing to file: {e}")

"""plot_filter_response - Plot the frequency response of the filter
@param sos - The second order sections
@param b - The numerator coefficients
@param a - The denominator coefficients
@return None"""
def plot_filter_response(sos, b, a):
    # Visualize filter characteristics
    w_sos, h_sos = sosfreqz(sos=sos, worN=8000, fs=sampling_rate)
    w_ba, h_ba = freqz(b, a, worN=8000, fs=sampling_rate)
    h_dB_sos = 20 * np.log10(np.abs(h_sos) + np.finfo(float).eps)  # Add a small epsilon to avoid log(0)
    h_dB_ba = 20 * np.log10(np.abs(h_ba) + np.finfo(float).eps)  # Add a small epsilon to avoid log(0)
    plt.figure()
    plt.plot(w_sos, h_dB_sos, 'b', label='SOS')
    plt.plot(w_ba, h_dB_ba, 'r', label='BA')
    plt.legend()
    plt.title(f"Frequency Response of {filter_type} {filter_mode} Filter")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.grid(True)

"""synthesize_filter_input - Synthesize a filter input signal
@param filter_mode - The filter mode
@param start_cutoff - The start cutoff frequency
@param stop_cutoff - The stop cutoff frequency
@param sampling_rate - The sampling rate
@param fname - The file name to write to
@return t - The time series
@return sinusoid - The sinusoid"""
def synthesize_filter_input(filter_mode, start_cutoff, stop_cutoff, sampling_rate, fname):
    # Generate and filter a sinusoid in the stop band
    if filter_mode == 'highpass':
        freq_in_stop_band = start_cutoff / 2
        freq_in_pass_band = start_cutoff * 2
    elif filter_mode == 'lowpass':
        freq_in_stop_band = start_cutoff * 2
        freq_in_pass_band = start_cutoff / 2
    elif filter_mode == 'bandstop':
        freq_in_stop_band = (start_cutoff + stop_cutoff) / 2
        freq_in_pass_band = start_cutoff / 2
    else:
        freq_in_stop_band = start_cutoff / 2
        freq_in_pass_band = (start_cutoff + stop_cutoff) / 2
        
    if verbose:
        print(f"Frequency in Stop Band: {freq_in_stop_band}")
        print(f"Frequency in Pass Band: {freq_in_pass_band}")

    # Generate a signal with the frequency in the stop band and the pass band, write it out to a file 
    # called example_data_sets/iir_test_signal.log
    t = np.linspace(0, 10.0, int(10.0 * sampling_rate), endpoint=False)
    sinusoid = np.sin(2 * np.pi * freq_in_stop_band * t) + np.sin(2 * np.pi * freq_in_pass_band * t)
    with open(fname, 'w') as f:
        # Modify time from seconds to milliseconds
        tms = t * 1000

        # Write the time series in column 0 and the sinusoid in column 1
        f.write("Time (ms),Sinusoid\n")
        for i in range(len(tms)):
            f.write(f"{tms[i]},{sinusoid[i]}\n")
    
    return t, sinusoid

"""test_c_filter_impl - Test the C filter implementation
@param fin - The input file
@param fout - The output file
@param filter_type - The filter type
@param filter_mode - The filter mode
@return filtered_signal - The filtered signal"""
def test_c_filter_impl(fin, fout, filter_type, filter_mode):
    c_args = f"./example_impl/filter_example -i {fin} -o {fout} -f {filter_type} -s {filter_mode}"
    
    try:
        # Clean and compile the application, change the working directory to example_impl
        os.chdir('example_impl')
        os.system("make clean")
        os.system("make")
        os.chdir('..')

        # Run the filter program with the test signal as input
        os.system(c_args)

        # Read the filtered signal from the file
        with open(fout, 'r') as f:
            lines = f.readlines()
            filtered_signal = np.zeros(len(lines) - 1)
            for i in range(1, len(lines) - 1):
                filtered_signal[i - 1] = float(lines[i].split(',')[1])
        
        return filtered_signal
    except Exception as e:
        print(f"Error running C filter implementation: {e}")

"""test_python_filter_impl - Test the Python filter implementation
@param sos - The second order sections
@param b - The numerator coefficients
@param a - The denominator coefficients
@param sinusoid - The sinusoid
@param use_sos - The use_sos flag
@return filtered_signal_python - The filtered signal in Python"""
def test_python_filter_impl(sos, b, a , sinusoid, use_sos):
    if use_sos:
        return sosfilt(sos, sinusoid)
    else:
        return lfilter(b, a, sinusoid)

"""fft_wrapper - Wrapper for the FFT
@param signal - The signal
@param sampling_rate - The sampling rate
@return frequency - The frequency
@return magnitude_dB - The magnitude in dB"""
def fft_wrapper(signal, sampling_rate):
    fs = sampling_rate
    N = len(signal)
    fft = np.fft.fft(signal)
    mag = np.abs(fft)
    magnitude_dB = 20 * np.log10(mag + 1e-12)  # Adding a small value to avoid log(0)
    frequency = np.linspace(0.0, fs/2, N//2)
    magnitude_dB = magnitude_dB[:N//2]
    return frequency, magnitude_dB

"""fft_filter_compare - Compare the FFT of the original signal and the filtered signal
@param sinusoid - The original signal
@param c_filt - The C filtered signal
@param py_filt - The Python filtered signal
@param sampling_rate - The sampling rate"""
def fft_filter_compare(sinusoid, c_filt, py_filt, sampling_rate):
    sig_freq, sig_mag = fft_wrapper(sinusoid, sampling_rate)
    c_freq, c_mag = fft_wrapper(c_filt, sampling_rate)
    py_freq, py_mag = fft_wrapper(py_filt, sampling_rate)

    plt.figure()
    plt.plot(sig_freq, sig_mag, 'b', label='Original Signal')
    plt.plot(c_freq, c_mag, 'r', label='Filtered Signal (C)')
    plt.plot(py_freq, py_mag, 'g', label='Filtered Signal (Python)')
    plt.legend()
    plt.title('FFT of Original and Filtered Signals')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)

# Create the parser
parser = argparse.ArgumentParser(description="IIR Filter Design")

# Add the arguments
parser.add_argument('-t', '--type', type=str, required=True, choices=['butter', 'cheby1', 'cheby2', 'ellip', 'bessel'], help="Filter type")
parser.add_argument('-m', '--mode', type=str, required=True, choices=['lowpass', 'highpass', 'bandpass', 'bandstop'], help="Filter mode")
parser.add_argument('-o', '--order', type=int, required=True, help="Filter order")
parser.add_argument('-s', '--sampling_rate', type=float, required=True, help="Sampling rate in Hz")
parser.add_argument('-c', '--start_cutoff', type=float, required=True, help="Start cutoff frequency in Hz")
parser.add_argument('-p', '--stop_cutoff', type=float, help="Optional stop cutoff frequency in Hz")
parser.add_argument('-u', '--use_sos', type=bool, default=False, help="Optional use_sos parameter")
parser.add_argument('-r', '--ripple', type=float, help="Optional ripple parameter for cheby1/2 and ellip filters")
parser.add_argument('-v', '--verbose', type=bool, default=False, help="Optional verbose parameter")

# Parse the arguments
args = parser.parse_args()

# Now you can access the values with args.type, args.mode, etc.
filter_type = args.type
filter_mode = args.mode
filter_order = args.order
sampling_rate = args.sampling_rate
start_cutoff = args.start_cutoff
stop_cutoff = args.stop_cutoff
use_sos = args.use_sos
ripple = args.ripple
verbose = args.verbose

# Calculate normalized cutoff frequencies
nyquist = 0.5 * sampling_rate
start_cutoff_normalized = start_cutoff / nyquist
stop_cutoff_normalized = stop_cutoff / nyquist if stop_cutoff else None

# Echo the parameters back to the user
print(f"Filter Type: {filter_type}")
print(f"Filter Mode: {filter_mode}")
print(f"Filter Order: {filter_order}")
print(f"Sampling Rate: {sampling_rate}")
print(f"Start Cutoff: {start_cutoff}")
print(f"Stop Cutoff: {stop_cutoff}")
print(f"Use SOS: {use_sos}")
print(f"Ripple: {args.ripple}")
print(f"Verbose: {verbose}")

# If we have a band stop or a band pass filter_mode, make sure there is a stop_cutoff
if filter_mode in ['bandpass', 'bandstop'] and not stop_cutoff:
    raise ValueError("Band pass and band stop filters require a stop cutoff frequency")

# Create the cricitical frequencies
if stop_cutoff:
    critical_freq = [start_cutoff_normalized, stop_cutoff_normalized]
else:
    critical_freq = start_cutoff_normalized
if verbose:
    print(f"Critical Frequencies: {critical_freq}")

# Generate filter coefficients
sos = iirfilter(N=filter_order, Wn=critical_freq, btype=filter_mode, ftype=filter_type, output='sos', fs=sampling_rate, rp=ripple)
b, a = iirfilter(N=filter_order, Wn=critical_freq, btype=filter_mode, ftype=filter_type, output='ba', fs=sampling_rate, rp=ripple)
if verbose:
    print(f"SOS: {sos}")
    print(f"B: {b}")
    print(f"A: {a}")

# Write the coefficients to a file
write_iir_coeffs(sos, b, a, 'impl/iir_filter/iir_coefficients.c')
write_iir_config(len(sos), filter_order, start_cutoff, stop_cutoff, 'impl/iir_filter/iir_config.h')


# Plot the frequency response of the filter
plot_filter_response(sos, b, a)

# Synthesize a filter input signal
t, sinusoid = synthesize_filter_input(filter_mode, start_cutoff, stop_cutoff, sampling_rate, 'example_data_sets/iir_test_signal.log')

# Test the C filter implementation
c_filter = "iir-biquad" if use_sos else "iir-ba"
filtered_signal = test_c_filter_impl('example_data_sets/iir_test_signal.log', 'example_data_sets/iir_filtered_signal.log', c_filter, filter_mode)

# Test the python filter implementation using the same coefficients
python_filter = test_python_filter_impl(sos, b, a, sinusoid, use_sos)

# Plot the FFT of different filter implementations and the original signal
fft_filter_compare(sinusoid, filtered_signal, python_filter, sampling_rate)

# Plot the original and filtered signals
plt.figure()
plt.plot(t, sinusoid, 'b', label='Original Signal')
plt.plot(t, filtered_signal, 'r', label='Filtered Signal (C)')
plt.plot(t, python_filter, 'g', label='Filtered Signal (Python)')
plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.title('Effectiveness of the Filter')
plt.show()

