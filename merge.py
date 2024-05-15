import pandas as pd

# Read the CSV and Excel files
csv_path = 'Comp_calcul_G_result_voice4PD.csv'
excel_path = 'ECOUTE-VOICE4PD-DEF_labels.xlsx'

csv_df = pd.read_csv(csv_path)
excel_df = pd.read_excel(excel_path)

# Extract patient names from filenames in the CSV
csv_df['Patient'] = csv_df['File'].str.split('-', expand=True)[1]

print(csv_df['Patient'])

# Extract patient names (first four characters) from the first column of the Excel file
# Extract only the first four characters from the 'Patient' column
# Extract only the first four characters from the first column 
excel_df['Patient'] = excel_df.iloc[:, 0].str[:4]
excel_df['Patient'] = excel_df.index.str[:4]



print(excel_df['Patient'])
# Merge the CSV and Excel dataframes based on the first four characters of the patient names
merged_df = csv_df.merge(excel_df[['Patient', 'Diagnostic', 'Moy-SEVERITE']], on='Patient', how='left')

# Select desired columns and potentially sort
result_df = merged_df[['Patient', 'Average Silence Duration', 'Speech Rate', 'Average Vowel Duration', 'Diagnostic', 'Moy-SEVERITE']]
# Fill blank Diagnostic rows with 'HC'
result_df['Diagnostic'].fillna('HC', inplace=True)

# Identify unmatched patient names
unmatched_patients = result_df[result_df['Diagnostic'].isnull() | result_df['Moy-SEVERITE'].isnull()]

# Save the merged dataframe to a new CSV file
result_csv_path = 'merged_patient_data.csv'
result_df.to_csv(result_csv_path, index=False)

# Print unmatched patient names
print("Unmatched Patient Names:")
print(unmatched_patients['Patient'].unique())

