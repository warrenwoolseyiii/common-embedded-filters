import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, cheby1, cheby2, freqz, sosfreqz, sosfilt, lfilter, firwin, firwin2, ellip, bessel
import argparse
import os

"""write_fir_coeffs - Write the FIR filter coefficients to a file
@param h - The filter coefficients
@param fname - The file name to write to
@return None"""
def write_fir_coeffs(h, fname):
    try:
        with open(fname, 'w') as f:
            f.write("// This is an auto generated file by filter_designer.py\n")
            f.write("// You can modify this manually or regenerate it by running filter_designer.py\n")
            f.write("// See the README for more information\n")
            f.write("#include \"fir_config.h\"\n")
            f.write("filter_coeff_t _fir_b_coeffs[FIR_NUM_COEFFS] = {\n")
            for i in range(len(h)):
                f.write(f"\t(filter_coeff_t)({h[i]}),\n")
            f.write("};\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

"""write_fir_config - Write the FIR filter configuration to a file
@param filter_order - The filter order
@param start_freq - The start frequency
@param stop_freq - The stop frequency
@param fname - The file name to write to
@return None"""
def write_fir_config(filter_order, start_freq, stop_freq, fname):
    try:
        if stop_freq is None:
            stop_freq = 0
        with open(fname, 'w') as f:
            f.write("// This is an auto generated file by filter_designer.py\n")
            f.write("// You can modify this manually or regenerate it by running filter_designer.py\n")
            f.write("// See the README for more information\n")
            f.write("#ifndef FIR_CONFIG_H_\n")
            f.write("#define FIR_CONFIG_H_\n")
            f.write("#include \"../filter_types.h\"\n")
            f.write(f"#define FIR_NUM_COEFFS {filter_order}\n")
            f.write(f"#define FIR_FILTER_ORDER {filter_order}\n")
            f.write(f"#define FIR_START_FREQ {start_freq}\n")
            f.write(f"#define FIR_STOP_FREQ {stop_freq}\n")
            f.write(f"extern filter_coeff_t _fir_b_coeffs[FIR_NUM_COEFFS];\n")
            f.write("#endif")
    except Exception as e:
        print(f"Error writing to file: {e}")

"""write_iir_coeffs - Write the IIR filter coefficients to a file, using both SOS and BA formats
@param sos - The second order sections
@param b - The numerator coefficients
@param a - The denominator coefficients
@param fname - The file name to write to
@return None"""
def write_iir_coeffs(sos, b, a, fname):
    try:
        with open(fname, 'w') as f:
            f.write("// This is an auto generated file by filter_designer.py\n")
            f.write("// You can modify this manually or regenerate it by running filter_designer.py\n")
            f.write("// See the README for more information\n")
            f.write("#include \"iir_config.h\"\n")
            f.write("filter_coeff_t _iir_b_coeffs[IIR_NUM_COEFFS] = {\n")
            for i in range(len(b)):
                f.write(f"\t(filter_coeff_t)({b[i]}),\n")
            f.write("};\n")
            f.write("filter_coeff_t _iir_a_coeffs[IIR_NUM_COEFFS] = {\n")
            for i in range(len(a)):
                f.write(f"\t(filter_coeff_t)({a[i]}),\n")
            f.write("};\n")
            f.write("filter_coeff_t _iir_sos_coeffs[IIR_BIQUAD_NUM_TERMS][6] = {\n")
            for i in range(len(sos)):
                f.write("{")
                for j in range(len(sos[i])):
                    f.write(f"(filter_coeff_t)({sos[i][j]}),")
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
            num_coeffs = filter_order + 1
        else:
            num_coeffs = (filter_order * 2) + 1
        with open(fname, 'w') as f:
            f.write("// This is an auto generated file by filter_designer.py\n")
            f.write("// You can modify this manually or regenerate it by running filter_designer.py\n")
            f.write("// See the README for more information\n")
            f.write("#ifndef IIR_CONFIG_H_\n")
            f.write("#define IIR_CONFIG_H_\n")
            f.write("#include \"../filter_types.h\"\n")
            f.write(f"#define IIR_BIQUAD_NUM_TERMS {num_terms}\n")
            f.write(f"#define IIR_NUM_COEFFS {num_coeffs}\n")
            f.write(f"#define IIR_FILTER_ORDER {filter_order}\n")
            f.write(f"#define IIR_START_FREQ {start_freq}\n")
            f.write(f"#define IIR_STOP_FREQ {stop_freq}\n")
            f.write(f"extern filter_coeff_t _iir_sos_coeffs[IIR_BIQUAD_NUM_TERMS][6];\n")
            f.write(f"extern filter_coeff_t _iir_b_coeffs[IIR_NUM_COEFFS];\n")
            f.write(f"extern filter_coeff_t _iir_a_coeffs[IIR_NUM_COEFFS];\n")
            f.write("#endif")
    except Exception as e:
        print(f"Error writing to file: {e}")

"""plot_iir_filter_response - Plot the frequency response of the filter
@param sos - The second order sections
@param b - The numerator coefficients
@param a - The denominator coefficients
@return None"""
def plot_iir_filter_response(sos, b, a, sampling_rate):
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

"""plot_fir_filter_response - Plot the frequency response of the filter
@param h - The filter coefficients
@return None"""
def plot_fir_filter_response(h, sampling_rate):
    w, h = freqz(h, worN=8000, fs=sampling_rate)
    h_dB = 20 * np.log10(np.abs(h) + np.finfo(float).eps)  # Add a small epsilon to avoid log(0)
    plt.figure()
    plt.plot(w, h_dB, 'b', label='FIR')
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
def synthesize_filter_input(filter_mode, frequencies, sampling_rate, fname):
    # Generate and filter a test signal, we need a frequency firmly in the stop band and one in the pass band
    if filter_mode == 'lowpass':
        freq_in_pass_band = np.random.uniform(0, frequencies[int(0)])
        freq_in_stop_band = np.random.uniform(frequencies[0], sampling_rate / 2)
    elif filter_mode == 'highpass':
        freq_in_pass_band = np.random.uniform(frequencies[0], sampling_rate / 2)
        freq_in_stop_band = np.random.uniform(0, frequencies[0])
    elif filter_mode == 'bandpass':
        # Find the bigger frequency range and put the stop band in the middle
        if nyquist - frequencies[1] > frequencies[0]:
            freq_in_stop_band = np.random.uniform(frequencies[1], nyquist)
        else:
            freq_in_stop_band = np.random.uniform(0, frequencies[0])
        freq_in_pass_band = np.random.uniform(frequencies[0], frequencies[1])
    elif filter_mode == 'bandstop':
        # Find the bigger frequency range and put the pass band in the middle
        if nyquist - frequencies[1] > frequencies[0]:
            freq_in_pass_band = np.random.uniform(frequencies[1], nyquist)
        else:
            freq_in_pass_band = np.random.uniform(0, frequencies[0])
        freq_in_stop_band = np.random.uniform(frequencies[0], frequencies[1])
    elif filter_mode == 'custom':
        # Choose any frequency in the frequency range that is not the 0th or last frequency
        freq_in_pass_band = np.random.choice(frequencies[1:-1])
        # Choose any frequency in between 0 and the sampling rate that is not in the frequency range
        while True:
            freq_in_stop_band = np.random.uniform(0, sampling_rate / 2)
            if freq_in_stop_band in frequencies or freq_in_stop_band == 0 or freq_in_stop_band == sampling_rate / 2:
                continue
            else:
                break

    if verbose:
        print(f"Frequency in Stop Band: {freq_in_stop_band}")
        print(f"Frequency in Pass Band: {freq_in_pass_band}")

    # Generate a signal with the frequency in the stop band and the pass band, write it out to a file 
    # called example_data_sets/iir_test_signal.log
    t = np.linspace(start=0, stop=10.0, num=10 * int(sampling_rate), endpoint=True)
    sinusoid = 100 * (np.sin(2 * np.pi * freq_in_stop_band * t) + np.sin(2 * np.pi * freq_in_pass_band * t))
    with open(fname, 'w') as f:
        # Modify time from seconds to milliseconds
        tms = t * 1000

        # Write the time series in column 0 and the sinusoid in column 1
        f.write("Time (ms),Sinusoid\n")
        for i in range(len(tms)):
            f.write(f"{tms[i]},{sinusoid[i]}\n")
    
    return t, sinusoid

"""test_c_filter_impl - Test the C filter implementation
@param c_args - The command line arguments for the C filter implementation
@param fout - The output file
@return filtered_signal - The filtered signal in C"""
def test_c_filter_impl(c_args, fout):    
    try:
        # Clean and compile the application, change the working directory to example_impl
        os.chdir('cmd_line_impl')
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

"""test_iir_python_filter_impl - Test the Python filter implementation
@param sos - The second order sections
@param b - The numerator coefficients
@param a - The denominator coefficients
@param sinusoid - The sinusoid
@param use_sos - The use_sos flag
@return filtered_signal_python - The filtered signal in Python"""
def test_iir_python_filter_impl(sos, b, a , sinusoid, use_sos):
    if use_sos:
        return sosfilt(sos, sinusoid)
    else:
        return lfilter(b, a, sinusoid)
    
"""test_fir_python_filter_impl - Test the Python filter implementation
@param h - The filter coefficients
@param sinusoid - The sinusoid
@return filtered_signal_python - The filtered signal in Python"""
def test_fir_python_filter_impl(h, sinusoid):
    return lfilter(h, 1, sinusoid)

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
    if debug:
        plt.plot(py_freq, py_mag, 'g', label='Filtered Signal (Python)')
    plt.legend()
    plt.title('FFT of Original and Filtered Signals')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)

# Create the parser
parser = argparse.ArgumentParser(description="Filter Designer")

# Add the arguments
parser.add_argument('-f', '--filter', type=str, default="", choices=['iir-biquad', 'iir', 'fir', 'fir-custom'], help="Filter type")
parser.add_argument('-m', '--mode', type=str, default="", choices=['lowpass', 'highpass', 'bandpass', 'bandstop', 'custom'], help="Filter mode")
parser.add_argument('-o', '--order', type=int, default=0, help="Filter order")
parser.add_argument('-s', '--sampling_rate', type=float, default=0, help="Sampling rate in Hz")
parser.add_argument('-c', '--start_cutoff', type=float, default=0, help="Start cutoff frequency in Hz")
parser.add_argument('-p', '--stop_cutoff', type=float, default=0, help="Optional stop cutoff frequency in Hz")
parser.add_argument('-r', '--ripple', type=float, default=None, help="Optional ripple parameter for cheby1/2 and ellip filters")
parser.add_argument('-v', '--verbose', type=bool, default=False, help="Optional verbose parameter")
parser.add_argument('-i', '--iir_filter_type', type=str, default='butter', choices=['butter', 'cheby1', 'cheby2', 'ellip', 'bessel'], help="Optional IIR filter type (default: butter)")
parser.add_argument('-w', '--window', type=str, default='hamming', choices=['hamming', 'hann', 'blackman', 'bartlett', 'boxcar'], help="Optional window for FIR filter design (default: hamming)")
parser.add_argument('-a', '--fir_algorithm', type=str, default='firwin', choices=['firwin2', 'firls', 'remez'], help="Optional FIR filter design algorithm (default: firwin)")
parser.add_argument('-d', '--debug', type=bool, default=False, help="Optional debug parameter")
parser.add_argument('-t', '--attenuition', type=float, default=0.1, help="Optional stopband attenuation for cheby1/2 and ellip filters")
parser.add_argument('-e', '--config_file', type=str, default="", help="Optional configuration file to bypass the command line arguments")
parser.add_argument('-l', '--roll_off', type=float, default=None, help="Optional roll off for the FIR filter")
parser.add_argument('-fr', '--frequency_range', nargs='+', default=None, help="Optional frequency range for firwin2 filter design algorithm")
parser.add_argument('-fg', '--frequency_gain', nargs='+', default=None, help="Optional frequency gain for firwin2 filter design algorithm")
parser.add_argument('-n', '--normalization', type=str, default='phase', choices=['phase', 'delay', 'mag'], help="Optional normalization for the frequency response for a bessel iir filter")

# Parse the arguments
args = parser.parse_args()

# Now you can access the values with args.type, args.mode, etc.
filter_type = args.filter
filter_mode = args.mode
filter_order = args.order
sampling_rate = args.sampling_rate
start_cutoff = args.start_cutoff
stop_cutoff = args.stop_cutoff
ripple = args.ripple
verbose = args.verbose
iir_filter_type = args.iir_filter_type
fir_window = args.window
fir_algorithm = args.fir_algorithm
debug = args.debug
attenuition = args.attenuition
roll_off = args.roll_off
config_file = args.config_file
frequency_range = args.frequency_range
frequency_gain = args.frequency_gain
norm = args.normalization
if config_file:
    try:
        with open(config_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                key, value = line.split('=')
                key = key.strip()
                value = value.strip()
                print(f"Key: {key}, Value: {value}")
                if value == "None":
                    print("Value is None")
                    continue
                if key == 'filter':
                    filter_type = value
                elif key == 'mode':
                    filter_mode = value
                elif key == 'order':
                    filter_order = int(value)
                elif key == 'sampling_rate':
                    sampling_rate = float(value)
                elif key == 'start_cutoff':
                    start_cutoff = float(value)
                elif key == 'stop_cutoff':
                    stop_cutoff = float(value)
                elif key == 'ripple':
                    ripple = float(value)
                elif key == 'verbose':
                    verbose = bool(value)
                elif key == 'iir_filter_type':
                    iir_filter_type = value
                elif key == 'window':
                    fir_window = value
                elif key == 'fir_algorithm':
                    fir_algorithm = value
                elif key == 'debug':
                    debug = bool(value)
                elif key == 'attenuition':
                    attenuition = float(value)
                elif key == 'roll_off':
                    roll_off = float(value)
                elif key == 'frequency_range':
                    frequency_range = list(map(float, value.split(',')))
                elif key == 'frequency_gain':
                    frequency_gain = list(map(float, value.split(',')))
                elif key == 'normalization':
                    norm = value
                config_success = True
    except Exception as e:
        print(f"Error reading from file: {e}")

use_sos = True if filter_type == 'iir-biquad' else False

# Calculate normalized cutoff frequencies, make everything a bandpass or bandstop filter
nyquist = 0.5 * sampling_rate
start_cutoff_normalized = start_cutoff / nyquist
if stop_cutoff:
    stop_cutoff_normalized = stop_cutoff / nyquist

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
print(f"IIR Filter Type: {iir_filter_type}")
print(f"FIR Window: {fir_window}")
print(f"FIR Algorithm: {fir_algorithm}")
print(f"Debug: {debug}")

# Print the scipy version
import scipy
print(f"Scipy Version: {scipy.__version__}")

# If we have a band stop or a band pass filter_mode, make sure there is a stop_cutoff
if filter_mode in ['bandpass', 'bandstop'] and not stop_cutoff:
    raise ValueError("Band pass and band stop filters require a stop cutoff frequency")

# Generate filter coefficients for an IIR filter
if filter_type == 'iir-biquad' or filter_type == 'iir':

    # Handle the different IIR filter design algorithms
    if iir_filter_type == 'butter':
        if filter_mode == 'lowpass' or filter_mode == 'highpass':
            # For high and low pass, butter expects a single critical frequency
            critical_freq = start_cutoff
        else:
            # For band pass and band stop, butter expects a tuple of critical frequencies
            critical_freq = []
            for i in range(int(stop_cutoff - start_cutoff) + 1):
                critical_freq.append(start_cutoff + i)
        
        if verbose:
            print(f"Critical Frequencies: {critical_freq}")
        
        # Generate the filter coefficients
        sos = butter(N=filter_order, Wn=critical_freq, btype=filter_mode, output='sos', fs=sampling_rate)
        b, a = butter(N=filter_order, Wn=critical_freq, btype=filter_mode, output='ba', fs=sampling_rate)
    elif iir_filter_type == 'cheby1':
        if filter_mode == 'lowpass' or filter_mode == 'highpass':
            # For high and low pass, cheby1 expects a single critical frequency
            critical_freq = start_cutoff_normalized
        else:
            # For band pass and band stop, cheby1 expects a tuple of critical frequencies
            critical_freq = [start_cutoff_normalized, stop_cutoff_normalized]
        
        if verbose:
            print(f"Critical Frequencies: {critical_freq}")
        
        # Generate the filter coefficients
        sos = cheby1(N=filter_order, rp=ripple, Wn=critical_freq, btype=filter_mode, output='sos')
        b, a = cheby1(N=filter_order, rp=ripple, Wn=critical_freq, btype=filter_mode, output='ba')
    elif iir_filter_type == 'cheby2':
        if filter_mode == 'lowpass' or filter_mode == 'highpass':
            # For high and low pass, cheby2 expects a single critical frequency
            critical_freq = start_cutoff_normalized
        else:
            # For band pass and band stop, cheby2 expects a tuple of critical frequencies
            critical_freq = [start_cutoff_normalized, stop_cutoff_normalized]
        
        if verbose:
            print(f"Critical Frequencies: {critical_freq}")
        
        # Generate the filter coefficients
        sos = cheby2(N=filter_order, rs=attenuition, Wn=critical_freq, btype=filter_mode, output='sos')
        b, a = cheby2(N=filter_order, rs=attenuition, Wn=critical_freq, btype=filter_mode, output='ba')
    elif iir_filter_type == 'ellip':
        if filter_mode == 'lowpass' or filter_mode == 'highpass':
            # For high and low pass, ellip expects a single critical frequency
            critical_freq = start_cutoff_normalized
        else:
            # For band pass and band stop, ellip expects a tuple of critical frequencies
            critical_freq = [start_cutoff_normalized, stop_cutoff_normalized]
        
        if verbose:
            print(f"Critical Frequencies: {critical_freq}")
        
        # Generate the filter coefficients
        sos = ellip(N=filter_order, rp=ripple, rs=attenuition, Wn=critical_freq, btype=filter_mode, output='sos')
        b, a = ellip(N=filter_order, rp=ripple, rs=attenuition, Wn=critical_freq, btype=filter_mode, output='ba')
    elif iir_filter_type == 'bessel':
        if filter_mode == 'lowpass' or filter_mode == 'highpass':
            # For high and low pass, bessel expects a single critical frequency
            critical_freq = start_cutoff_normalized
        else:
            # For band pass and band stop, bessel expects a tuple of critical frequencies
            critical_freq = [start_cutoff_normalized, stop_cutoff_normalized]
        
        if verbose:
            print(f"Critical Frequencies: {critical_freq}")
        
        # Generate the filter coefficients
        sos = bessel(N=filter_order, norm=norm, Wn=critical_freq, btype=filter_mode, output='sos')
        b, a = bessel(N=filter_order, norm=norm, Wn=critical_freq, btype=filter_mode, output='ba')
    else:
        raise ValueError("Unknown IIR filter design algorithm")

    if verbose:
        print(f"SOS: {sos}")
        print(f"B: {b}")
        print(f"A: {a}")

    # Write the coefficients to a file
    write_iir_coeffs(sos, b, a, 'impl/iir_filter/iir_coefficients.c')
    write_iir_config(len(sos), filter_order, start_cutoff, stop_cutoff, 'impl/iir_filter/iir_config.h')


    # Plot the frequency response of the filter
    plot_iir_filter_response(sos, b, a, sampling_rate)

    # Synthesize a filter input signal
    iir_signal = 'example_data_sets/iir_test_signal.log'
    iir_out_signal = 'example_data_sets/iir_filtered_signal.log'
    t, sinusoid = synthesize_filter_input(filter_mode, [start_cutoff, stop_cutoff], sampling_rate, iir_signal)

    # Test the C filter implementation
    c_filter = "iir-biquad" if use_sos else "iir"
    c_args = f"./cmd_line_impl/filter_example -i {iir_signal} -o {iir_out_signal} -f {c_filter} -s {filter_mode}"
    filtered_signal = test_c_filter_impl(c_args, iir_out_signal)

    # Test the python filter implementation using the same coefficients
    python_filter = test_iir_python_filter_impl(sos, b, a, sinusoid, use_sos)

    # Plot the FFT of different filter implementations and the original signal
    fft_filter_compare(sinusoid, filtered_signal, python_filter, sampling_rate)

    # Plot the original and filtered signals
    plt.figure()
    plt.plot(t, sinusoid, 'b', label='Original Signal')
    plt.plot(t, filtered_signal, 'r', label='Filtered Signal (C)')
    if debug:   
        plt.plot(t, python_filter, 'g', label='Filtered Signal (Python)')
    plt.legend()
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.title('Effectiveness of the Filter')
    plt.show()
elif filter_type == 'fir' or filter_type == 'fir-custom':
    # Create the cricitical frequencies
    if stop_cutoff:
        critical_freq = [start_cutoff, stop_cutoff]
    else:
        critical_freq = [start_cutoff]

    if verbose:
        print(f"Critical Frequencies: {critical_freq}")

    if fir_algorithm == 'firwin':
        h = firwin(numtaps=filter_order, cutoff=critical_freq, window=fir_window, width=roll_off, fs=sampling_rate, pass_zero=filter_mode)
    elif fir_algorithm == 'firwin2':
        # Ensure that a frequency range is provided
        if not frequency_range:
            raise ValueError("firwin2 requires a frequency range")
        
        # Populate a full set of frequency ranges and gains, we assume if the frequency is in the range, it is a pass band
        critical_freq = []
        target_gain = []
        for i in range(int(sampling_rate/2) + 1):
            critical_freq.append(i)
            if i in frequency_range and i != 0 and i != sampling_rate / 2:
                if frequency_gain:
                    target_gain.append(frequency_gain[frequency_range.index(i)])
                else:
                    target_gain.append(1)
            else:
                target_gain.append(0)
        
        # Generate the filter coefficients
        h = firwin2(numtaps=filter_order, freq=critical_freq , gain=target_gain, window=fir_window, fs=sampling_rate)

        # Reset this value to only the pass band frequencies for the test signal
        critical_freq = frequency_range
    elif fir_algorithm == 'firls':
        # h = firls(numtaps=filter_order, freq=critical_freq, gain=[1, 0], fs=sampling_rate)
        raise ValueError("firls is not supported")
    elif fir_algorithm == 'remez':
        # h = remez(numtaps=filter_order, bands=[0, start_cutoff, stop_cutoff, nyquist], desired=[1, 0], fs=sampling_rate)
        raise ValueError("remez is not supported")
    else:
        raise ValueError("Unknown FIR filter design algorithm")

    if verbose:
        print(f"H: {h}")

    # Write the coefficients to a file
    write_fir_coeffs(h, 'impl/fir_filter/fir_coefficients.c')
    write_fir_config(filter_order, start_cutoff, stop_cutoff, 'impl/fir_filter/fir_config.h')

    # Plot the frequency response of the filter
    plot_fir_filter_response(h, sampling_rate)

    # Synthesize a filter input signal
    fir_signal = 'example_data_sets/fir_test_signal.log'
    fir_out_signal = 'example_data_sets/fir_filtered_signal.log'
    t, sinusoid = synthesize_filter_input(filter_mode, critical_freq, sampling_rate, fir_signal)

    # Test the C filter implementation
    c_args = f"./cmd_line_impl/filter_example -i {fir_signal} -o {fir_out_signal} -f fir -s {filter_mode}"
    filtered_signal = test_c_filter_impl(c_args, fir_out_signal)

    # Test the python filter implementation using the same coefficients
    python_filter = test_fir_python_filter_impl(h, sinusoid)

    # Plot the FFT of different filter implementations and the original signal
    fft_filter_compare(sinusoid, filtered_signal, python_filter, sampling_rate)

    # Plot the original and filtered signals
    plt.figure()
    plt.plot(t, sinusoid, 'b', label='Original Signal')
    plt.plot(t, filtered_signal, 'r', label='Filtered Signal (C)')
    if debug:
        plt.plot(t, python_filter, 'g', label='Filtered Signal (Python)')
    plt.legend()
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.title('Effectiveness of the Filter')
    plt.show()

