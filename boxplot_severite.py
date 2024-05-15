import pandas as pd
import matplotlib.pyplot as plt

# Read the merged data
merged_df = pd.read_csv('merged_patient_data.csv')

# Filter the DataFrame to include only 'PD' and 'MSA-P' values in the 'Diagnostic' column
filtered_df = merged_df[merged_df['Diagnostic'].isin(['PD', 'MSA-P'])]

# Convert 'Moy-SEVERITE' column to numeric
filtered_df['Moy-SEVERITE'] = pd.to_numeric(filtered_df['Moy-SEVERITE'], errors='coerce')

# Define the ranges for severities
severity_ranges = [(3, 6), (6.1, 8), (8.1, 8.6)]

# Plot boxplots for each parameter and each severity range
parameters = ['Average Silence Duration', 'Speech Rate', 'Average Vowel Duration']
for param in parameters:
    plt.figure(figsize=(15, 6))  # Larger figure size
    for i, (low, high) in enumerate(severity_ranges, start=1):
        plt.subplot(1, 3, i)
        grouped_df = filtered_df[(filtered_df['Moy-SEVERITE'] >= low) & (filtered_df['Moy-SEVERITE'] <= high)]
        grouped_df.boxplot(column=param, by='Diagnostic', ax=plt.gca())
        plt.title('Severity Range {}-{}'.format(low, high))
        plt.xlabel('Diagnostic')
        plt.ylabel(param)
    plt.suptitle('Boxplot of {}'.format(param), y=1.05)  # Adjust y position for main title
    plt.subplots_adjust(top=0.8)  # Adjust top margin
    plt.tight_layout()
    plt.savefig('{}_boxplots.png'.format(param))
    plt.show()

