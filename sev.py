import pandas as pd

# Read the Excel file
file_path = 'ECOUTE-VOICE4PD-DEF_labels.xlsx'
df = pd.read_excel(file_path)

# Fill blank cells in 'Diagnostic' column with 'HC'
df['Diagnostic'].fillna('HC', inplace=True)

# Filter rows for 'PD', 'HC', and 'MSA-P' in 'Diagnostic' column
filtered_df = df[df['Diagnostic'].isin(['PD', 'HC', 'MSA-P'])]

# Print separately the 'Diagnostic' and 'Moy-SEVERITE' columns for PD, HC, and MSA-P
for diagnostic_value in ['PD', 'HC', 'MSA-P']:
    print("Diagnostic: {}".format(diagnostic_value))
    diagnostic_rows = filtered_df[filtered_df['Diagnostic'] == diagnostic_value]
    diagnostic_rows_sorted = diagnostic_rows.sort_values(by='Moy-SEVERITE')
    print(diagnostic_rows_sorted[['Diagnostic', 'Moy-SEVERITE']])
    print()

