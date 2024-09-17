import pandas as pd
import os

# Define input and output directories
input_dir = r'C:\Users\Dr. Contessa Petrini\ChemPath\TCMSP-Spider\data\spider_data'
output_dir = r'C:\Users\Dr. Contessa Petrini\ChemPath\TCMSP-Spider\data\cleaned_data'

def clean_data(file_name):
    # Load data
    file_path = os.path.join(input_dir, file_name)
    
    if not os.path.exists(file_path):
        print(f'File not found: {file_path}')
        return
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f'Error reading {file_name}: {e}')
        return

    # Basic cleaning steps (modify as needed)
    df.dropna(inplace=True)  # Remove rows with missing values
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # Strip whitespace from string columns
    df.columns = [col.strip().lower() for col in df.columns]  # Normalize column names

    # Save the cleaned data
    output_path = os.path.join(output_dir, file_name)
    df.to_excel(output_path, index=False)

def main():
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all Excel files in the input directory
    excel_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx')]

    # Clean each file
    for file_name in excel_files:
        print(f'Cleaning {file_name}...')
        clean_data(file_name)
        print(f'{file_name} cleaned and saved to {output_dir}')

if __name__ == '__main__':
    main()
