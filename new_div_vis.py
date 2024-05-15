import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("G_result_new_division.csv")

# Group the DataFrame by file and type
grouped = df.groupby(["File", "Type"])
"""
# Plot the speech rate for each group
for (file, type), group in grouped:
    plt.figure()
    plt.plot(group["Start"], group["Speech Rate"], marker='o')
    plt.title("{} - {}".format(file, type))
    plt.xlabel("Start Time")
    plt.ylabel("Speech Rate")
    plt.grid(True)
    plt.savefig("{}_{}_speech_rate.png".format(file, type))  # Save the plot as an image
    plt.show()  # Show the plot
    plt.close()  # Close the plot to release memory

"""
# Iterate over each file
for filename in df['File'].unique():
    # Filter data for the current file
    file_data = df[df['File'] == filename]
    
    # Split data into "manuel" and "auto" types
    manuel_data = file_data[file_data['Type'] == 'manuel']
    auto_data = file_data[file_data['Type'] == 'auto']
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(manuel_data['Start'], manuel_data['Speech Rate'], marker='o', linestyle='-', label='manuel')
    plt.plot(auto_data['Start'], auto_data['Speech Rate'], marker='o', linestyle='-', label='auto')
    
    # Add labels and title
    plt.xlabel('Start Time')
    plt.ylabel('Speech Rate')
    plt.title('Speech Rate Variation for {}'.format(filename))
    
    # Add legend
    plt.legend()
    
    # Save the plot as an image
    plt.savefig("{}_variation_speech_rate.png".format(filename))
    plt.show()  # Show the plot
    plt.close()  # Close the plot to release memory


# Calculate the average speech rate and variance for each file
average_speech_rate = grouped["Speech Rate"].mean()
variance_speech_rate = grouped["Speech Rate"].var()

# Iterate over each file
for filename, file_data in grouped:
    # Plot all speech rates for the current file
    plt.figure(figsize=(10, 6))
    plt.plot(file_data['Start'], file_data['Speech Rate'], marker='o', linestyle='-', label='Speech Rate')
    
    # Plot the average speech rate as a line
    plt.axhline(y=average_speech_rate[filename], color='r', linestyle='--', label='Average Speech Rate')
    
    # Add labels and title
    plt.xlabel('Start Time')
    plt.ylabel('Speech Rate')
    plt.title('Speech Rate Variation for {} (Variance: {:.4f})'.format(filename, variance_speech_rate[filename]))
    
    # Add legend
    plt.legend()
    
    # Save the plot as an image
    plt.savefig("{}_speech_rate_variation_with_avg.png".format(filename))
    plt.show()  # Show the plot
    plt.close()  # Close the plot to release memory


