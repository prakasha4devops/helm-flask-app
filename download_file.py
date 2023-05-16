import requests
import json

def download_file_with_auth(url, username, password):
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return response.content
    else:
        return None

def convert_to_json(file_content):
    try:
        json_data = json.loads(file_content)
        return json_data
    except json.JSONDecodeError:
        return None

# Example usage
url = "http://example.com/file.txt"
username = "your_username"
password = "your_password"

file_content = download_file_with_auth(url, username, password)
if file_content is not None:
    json_data = convert_to_json(file_content)
    if json_data is not None:
        # Process the JSON data as needed
        print(json_data)
    else:
        print("Failed to convert file content to JSON.")
else:
    print("Failed to download file.")
