import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
data = pd.read_csv('G_result_division_textgrid_new.csv')


# Get unique file names
file_names = data['File'].unique()

# Create boxplots for each file
for file_name in file_names:
    file_data = data[data['File'] == file_name]
    metrics = ['Average Silence Duration', 'Speech Rate', 'Average Vowel Duration']

    for metric in metrics:
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Part', y=metric, hue='Type', data=file_data)
        plt.title('{} - {} by Part and Type'.format(file_name, metric))
        plt.xlabel('Part')
        plt.ylabel(metric)
        plt.legend(title='Type', loc='upper right')
        plt.savefig('vis_generale_{}_{}_new.png'.format(file_name,metric))  # Saving each box plot as a separate file
        plt.show()

