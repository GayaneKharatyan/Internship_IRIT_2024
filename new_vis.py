import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("G_result_new_division.csv")

# Group the DataFrame by file and type
grouped = df.groupby(["File"])


# Iterate over each file
for filename, file_data in grouped:
    # Sort the data by 'Start' time
    file_data = file_data.sort_values(by='Start')

    # Initialize lists to store plotted points for "manuel" and "auto"
    manuel_points = []
    auto_points = []


    for type_name, type_data in file_data.groupby("Type"):
        color = 'blue' if type_name == 'manuel' else 'orange'  # Assign color based on type

        for i, row in type_data.iterrows():
            # Plot the points and store them in respective lists
            plt.plot(row['Start'], row['Speech Rate'], marker='o', color=color)  # Removed label parameter
            if type_name == 'manuel':
                manuel_points.append((row['Start'], row['Speech Rate']))
            else:
                auto_points.append((row['Start'], row['Speech Rate']))

    # Draw lines for "manuel" points if both "manuel" and "auto" points exist
    if manuel_points and auto_points:
        for manuel_point in manuel_points:
            for auto_point in auto_points:
                # Check if the difference in x-coordinates is <= 1
                if abs(manuel_point[0] - auto_point[0]) <= 1:
                    plt.plot([manuel_point[0], auto_point[0]], 
                             [manuel_point[1], auto_point[1]], 
                             color='grey', linestyle='--')  # dashed grey lines
    
    # Draw horizontal lines for the last "manuel" and "auto" points until the start of the next point
    if manuel_points:
        for i in range(len(manuel_points) - 1):
            plt.hlines(y=manuel_points[i][1], xmin=manuel_points[i][0], xmax=manuel_points[i + 1][0], color='blue')
        plt.hlines(y=manuel_points[-1][1], xmin=manuel_points[-1][0], xmax=file_data['Start'].max(), color='blue')
        plt.plot([manuel_points[-1][0], file_data['Start'].max()], [manuel_points[-1][1], manuel_points[-1][1]], color='blue')
    if auto_points:
        for i in range(len(auto_points) - 1):
            plt.hlines(y=auto_points[i][1], xmin=auto_points[i][0], xmax=auto_points[i + 1][0], color='orange')
        plt.hlines(y=auto_points[-1][1], xmin=auto_points[-1][0], xmax=file_data['Start'].max(), color='orange')
        plt.plot([auto_points[-1][0], file_data['Start'].max()], [auto_points[-1][1], auto_points[-1][1]], color='orange')

    # Draw horizontal dashed lines for the last "manuel" and "auto" points until the end of the x-axis
    if manuel_points:
        manuel_last_point = manuel_points[-1]
        plt.hlines(y=manuel_last_point[1], xmin=manuel_last_point[0], xmax=plt.xlim()[1], color='blue')
    if auto_points:
        auto_last_point = auto_points[-1]
        plt.hlines(y=auto_last_point[1], xmin=auto_last_point[0], xmax=plt.xlim()[1], color='orange')
        
    # Calculate the x-coordinate for the end of the x-axis
    end_of_x_axis = file_data['Start'].max()

    # Extend lines for the last "manuel" and "auto" points till the end of x-axis
    if manuel_points:
        plt.plot([manuel_points[-1][0], end_of_x_axis], [manuel_points[-1][1], manuel_points[-1][1]], color='blue')
    if auto_points:
        plt.plot([auto_points[-1][0], end_of_x_axis], [auto_points[-1][1], auto_points[-1][1]], color='orange')
        
    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Speech Rate')
    plt.title('Speech Rate Variation for {}'.format(filename))
# Create legend outside of loop
    plt.plot([], marker='o', color='blue', label='manuel')
    plt.plot([], marker='o', color='orange', label='auto')
    plt.legend()
    # Save the plot as an image
    plt.savefig("{}_new_variation_speech_rate.png".format(filename))
    plt.show()  # Show the plot
    plt.close()  # Close the plot to release memory



