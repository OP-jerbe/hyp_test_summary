"""
This script is used to fix the csv files from test stand 1 and 2, both of
which output the wrong sign on the Beam Voltage data.
"""

import os

import pandas as pd

from dir_path import DIR_PATH

# Set the directory where your CSV files are located
directory = DIR_PATH

# Loop through all CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Construct full file path
        file_path = os.path.join(directory, filename)

        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if column 'Beam Voltage (kV)' exists
        if 'Beam Voltage (kV)' in df.columns:
            # Flip the sign of column 'D'
            df['Beam Voltage (kV)'] = -df['Beam Voltage (kV)']

            # Save the modified DataFrame back to CSV
            df.to_csv(file_path, index=False)
            print(f'Processed {filename}')
        else:
            print(f"Column 'Beam Voltage (kV)' not found in {filename}")

print('All files processed.')
