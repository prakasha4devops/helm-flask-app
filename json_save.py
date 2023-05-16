import requests
import pandas as pd
import json

def download_excel_with_auth(url, username, password):
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return response.content
    else:
        return None

def convert_excel_tab_to_json(excel_content, sheet_name):
    try:
        df = pd.read_excel(excel_content, sheet_name=sheet_name)
        json_data = df.to_json(orient='records')
        return json_data
    except Exception as e:
        print("Error occurred while converting Excel tab to JSON:", str(e))
        return None

def save_json_to_file(json_data, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json_file.write(json_data)
        print("JSON data saved to", file_path)
    except Exception as e:
        print("Error occurred while saving JSON data:", str(e))

# Example usage
url = "http://example.com/file.xlsx"
username = "your_username"
password = "your_password"
sheet_name = "Sheet1"
output_file = "output.json"

excel_content = download_excel_with_auth(url, username, password)
if excel_content is not None:
    json_data = convert_excel_tab_to_json(excel_content, sheet_name)
    if json_data is not None:
        save_json_to_file(json_data, output_file)
    else:
        print("Failed to convert Excel tab to JSON.")
else:
    print("Failed to download Excel file.")
