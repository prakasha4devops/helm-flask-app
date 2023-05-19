import requests
import yaml
from getpass import getpass

# Jira API credentials and base URL
username = input("Enter your Jira username: ")
password = getpass("Enter your Jira password: ")
base_url = "https://your-jira-instance.atlassian.net/rest/api/2/"

# Parse YAML file
with open('ticket_data.yaml') as file:
    data = yaml.safe_load(file)

# Create a session
session = requests.Session()
session.auth = (username, password)

# Create the main ticket
ticket_data = {
    "fields": {
        "project": {"key": data['project_key']},
        "summary": data['main_summary'],
        "description": data['main_description'],
        "issuetype": {"name": "Task"},
        "assignee": {"name": data['main_assignee']},
        "reporter": {"name": data['main_reporter']}
    }
}

create_ticket_url = base_url + "issue"
response = session.post(create_ticket_url, json=ticket_data)

