import pandas as pd
import matplotlib.pyplot as plt

# Reading the CSV file into a pandas DataFrame
df = pd.read_csv('G_result_voice4PD.csv')

# Extracting patient type from the file name
def extract_patient_type(file_name):
    return file_name.split('-')[0][-2:]

df['Patient Type'] = df['File'].apply(lambda x: extract_patient_type(x.split('/')[-1]))

# Creating a combined dataset for each metric
combined_data = {}
for metric in ['Average Silence Duration', 'Speech Rate', 'Average Vowel Duration']:
    metric_data = []
    labels = []
    for part in range(1, 4):
        for patient_type in ['HC', 'PD', 'SA']:
            part_data = df[(df['Part'] == part) & (df['Patient Type'] == patient_type)][metric]
            metric_data.append(part_data)
            labels.append('{} part {}'.format(patient_type, part))

    combined_data[metric] = (metric_data, labels)

# Creating box plots for each metric
for metric, (data, labels) in combined_data.items():
    plt.figure(figsize=(10, 6))
    plt.boxplot(data, labels=labels)
    plt.title('Box Plot for {}'.format(metric))
    plt.xlabel('Patient Type - Part')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('boxplot_generale_{}.png'.format(metric))  # Saving each box plot as a separate file
    plt.show()

