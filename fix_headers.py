"""
This script is used to fix the csv files from test stand 1 and 2, both of
which output the wrong sign on the Beam Voltage and Exctractor voltage data.
Also fixes the Lens #1 Voltage header to display the correct unit.
"""

import os

import pandas as pd

# Set the directory where your CSV files are located
directory: str = ''

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
        else:
            print(f"Column 'Beam Voltage (kV)' not found in {filename}")

        if 'Lens #1 Voltage (kV)' in df.columns:
            # Change the unit from kV to V
            df = df.rename(columns={'Lens #1 Voltage (kV)': 'Lens #1 Voltage (V)'})
        else:
            print(f"Column 'Lens #1 Voltage (kV)' not found in {filename}")

        if 'Extractor Voltage (kV)' in df.columns:
            # Flip the sign of column 'F'
            df['Extractor Voltage (kV)'] = -df['Extractor Voltage (kV)']
        else:
            print(f"Column 'Extractor Voltage (kV)' not found in {filename}")

        # Save the modified DataFrame back to CSV
        df.to_csv(file_path, index=False)
        print(f'Processed {filename}')

print('All files processed.')
