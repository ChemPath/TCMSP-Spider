import os
import pandas as pd
import requests
from supabase import create_client, Client
from tcmsp import TcmspSpider  # Assuming TcmspSpider and get_data are in tcmsp.py

# Supabase configuration
SUPABASE_URL = 'https://lqwxjiijnhefterkeety.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxxd3hqaWlqbmhlZnRlcmtlZXR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNjU5NTk3OSwiZXhwIjoyMDQyMTcxOTc5fQ.bmEG-1VU5MgU9TAWsXS0FEwVpH3qgc49dyUqXxvK3Kk'
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set up headers for REST API requests
headers = {
    'Content-Type': 'application/json',
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

# Directory where the new data files are stored
data_directory = 'C:/Users/Dr. Contessa Petrini/ChemPath/src/data/cleaned_data/'

# Function to insert data into Supabase
def insert_data(file_path, table_name, supabase_client):
    df = pd.read_excel(file_path)

    if table_name == 'ingredients':
        herb_name = os.path.basename(file_path).split('_')[0]
        herb_id = 1  # Replace with the actual herb_id

        for index, row in df.iterrows():
            molecule_name = row['molecule_name'].replace("'", "''")
            response = requests.post(f'{SUPABASE_URL}/rest/v1/{table_name}', json={
                'name': molecule_name,
                'herb_id': herb_id,
                'quantity': None
            }, headers=headers)

            if response.status_code != 201:
                print(f"Error inserting into {table_name}: {response.text}")

    # Add additional logic for other table types here...

# Function to get data from TCM database using TcmspSpider
def get_data(data_type):
    tcmsp = TcmspSpider()
    url = f"https://tcmsp-e.com/browse.php?qc={data_type}"
    html = tcmsp.get_response(url)
    data = tcmsp.get_json_data(html, num=8, pattern="grid")
    
    # Save data to an Excel file
    tcmsp.text_to_excel(
        data,
        file_path=f"{data_directory}",
        file_name=f"{data_type}_data",
        index=False
    )

# Main script to get data and insert into Supabase
def main():
    type_list = ["herbs", "ingredients", "targets", "diseases"]

    # Fetch the data using get_data
    for data_type in type_list:
        print(f"Fetching data for: {data_type}")
        get_data(data_type)  # This will save the data to Excel files

        # File path to the newly created Excel file
        file_path = os.path.join(data_directory, f"{data_type}_data.xlsx")
        if os.path.exists(file_path):
            print(f"Inserting data for: {data_type}")
            insert_data(file_path, data_type, supabase_client)
        else:
            print(f"File not found: {file_path}")

if __name__ == '__main__':
    main()
