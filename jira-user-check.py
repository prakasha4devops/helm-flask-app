import requests
from getpass import getpass

# Jira API credentials and base URL
username = input("Enter your Jira username: ")
password = getpass("Enter your Jira password: ")
base_url = "https://your-jira-instance.atlassian.net/rest/api/2/"

# Email ID to check
email_id = "example@example.com"  # Replace with the email ID you want to check

# Create a session
session = requests.Session()
session.auth = (username, password)

# Check if user exists
def check_user_exists(email):
    user_url = base_url + "user/search"
    params = {
        "query": email
    }
    response = session.get(user_url, params=params)
    if response.status_code == 200:
        user_data = response.json()
        return len(user_data) > 0
    return False

if check_user_exists(email_id):
    print(f"User with email ID '{email_id}' exists in Jira.")
else:
    print(f"User with email ID '{email_id}' does not exist in Jira.")
