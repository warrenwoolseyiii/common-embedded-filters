import sys
import matplotlib.pyplot as plt
import numpy as np

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

"""find_sample_rate - Find the sample rate from time stamps
@param time - The time stamps
@return sample_rate - The sample rate in Hz"""
def find_sample_rate(time_series):
    # Calculate the average time difference between all samples in the time series
    time_diff = np.diff(time_series) / 1000.0  # Convert to seconds
    sample_rate = 1 / np.mean(time_diff)
    return sample_rate

"""read_file - Read a CSV file
@param file_name - The file name
@return header - The header
@return data - The data"""
def read_file(file_name):
    data = []
    header = []
    header_read = False
    with open(file_name, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                if not header_read:
                    header = line.strip().split(',')
                    header_read = True
                else:
                    data.append(line.strip().split(','))
    return header, data

"""plot_subplots - Plot the FFT results in a comparison plot
@param plot_names - The plot names
@param plot_headers - The plot headers
@param set1 - The first set of data
@param set2 - The second set of data"""
def plot_subplots(plot_names, plot_headers, set1, set2):
    num_axes = len(plot_headers[0]) - 1
    _, ax = plt.subplots(num_axes, 1, figsize=(10, 8))
    if num_axes == 1:
        ax = [ax]
    for i in range(num_axes):
        ax[i].plot(set1[0], set1[1], label=plot_names[0])
        ax[i].plot(set2[0], set2[1], label=plot_names[1])
        ax[i].set_xlabel('Frequency (Hz)')
        ax[i].set_ylabel('Magnitude (dB)')
        ax[i].set_title('FFT Results')
        ax[i].legend(plot_names)
    plt.tight_layout()
    plt.show()

"""fft_compare - Compare the FFT results of two files
@param file_name1 - The first file name
@param file_name2 - The second file name"""
def fft_compare(file_name1, file_name2):
    header1, data1 = read_file(file_name1)
    fs1 = find_sample_rate([float(x[0]) for x in data1])
    time1, mag1 = fft_wrapper([float(x[1]) for x in data1], fs1)

    header2, data2 = read_file(file_name2)
    fs2 = find_sample_rate([float(x[0]) for x in data2])
    time2, mag2 = fft_wrapper([float(x[1]) for x in data2], fs2)

    plot_names = [file_name1, file_name2]
    plot_headers = [header1, header2]
    set1 = [time1, mag1]
    set2 = [time2, mag2]
    plot_subplots(plot_names, plot_headers, set1, set2)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Please provide two file names as arguments.')
        sys.exit(1)

    file_name1 = sys.argv[1]
    file_name2 = sys.argv[2]
    fft_compare(file_name1, file_name2)

