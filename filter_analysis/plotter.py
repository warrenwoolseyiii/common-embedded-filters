import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_csv_files(file1, file2):
    # Read the CSV files into pandas DataFrames
    df1 = pd.read_csv(file1)
    if file2 != "":
        df2 = pd.read_csv(file2)

    # Strip the first row from each DataFrame, these are the labels
    df1 = df1.iloc[1:]
    if file2 != "":
        df2 = df2.iloc[1:]
    
    # Extract the time column from each DataFrame
    time1 = df1.iloc[:, 0]
    if file2 != "":
        time2 = df2.iloc[:, 0]

    # Plot the remaining columns as series on the same chart
    for col in df1.columns[1:]:
        plt.plot(time1, df1[col], label=f'{col}')
    if file2 != "":
        for col in df2.columns[1:]:
            plt.plot(time2, df2[col], label=f'filtered - {col}')

    # Set the x-axis label
    plt.xlabel('Time')

    # Set the y-axis label
    plt.ylabel('Value')

    # Add a legend, place it in the bottom left corner
    plt.legend(loc='upper right', title='Series')

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python plotter.py <file1> <file2>")
        sys.exit(1)

    # Get the file paths from command line arguments
    file1 = sys.argv[1]
    if len(sys.argv) == 2:
        file2 = ""
    else:
        file2 = sys.argv[2]

    # Call the plot_csv_files function with the provided file paths
    plot_csv_files(file1, file2)


