"""
import pandas as pd
import matplotlib.pyplot as plt

#Reading the CSV file into a pandas DataFrame
df = pd.read_csv('G_result_voice4PD.csv')

#Extracting patient type from the file name
def extract_patient_type(file_name):
    return file_name.split('-')[0][-2:]

df['Patient Type'] = df['File'].apply(lambda x: extract_patient_type(x.split('/')[-1]))

#Grouping the data by 'Patient Type' and 'Part'
grouped = df.groupby(['Patient Type', 'Part'])

#Creating box plots for each group
for (patient_type, part), group_data in grouped:
    plt.figure()
    group_data.boxplot(column=['Average Silence Duration', 'Speech Rate', 'Average Vowel Duration'])
    plt.title('Box Plot for {} - Part {}'.format(patient_type, part))
    plt.ylabel('Values')
    plt.xlabel('Metrics')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('boxplot_{}_part_{}.png'.format(patient_type, part))  #Saving each box plot as a separate file
    plt.show()
"""


import pandas as pd
import matplotlib.pyplot as plt

# Reading the CSV file into a pandas DataFrame
df = pd.read_csv('G_result_voice4PD.csv')

# Extracting patient type from the file name
def extract_patient_type(file_name):
    return file_name.split('-')[0][-2:]

df['Patient Type'] = df['File'].apply(lambda x: extract_patient_type(x.split('/')[-1]))

# Grouping the data by 'Part' and 'Patient Type'
grouped = df.groupby(['Part', 'Patient Type'])

# Creating box plots for each metric for each part
metrics = ['Average Silence Duration', 'Speech Rate', 'Average Vowel Duration']
for metric in metrics:
    plt.figure(figsize=(10, 6))
    for part in sorted(df['Part'].unique()):
        part_data = []
        labels = []
        for patient_type, group_data in grouped:
            if part in group_data['Part'].values:
                part_data.append(group_data[group_data['Part'] == part][metric])
                labels.append(patient_type)
        plt.boxplot(part_data, labels=labels)
        plt.title('Box Plot for {} - Part {}'.format(metric, part))
        plt.xlabel('Patient Type')
        plt.ylabel('Values')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('boxplot_{}_part_{}.png'.format(metric, part))  # Saving each box plot as a separate file

        plt.show()

