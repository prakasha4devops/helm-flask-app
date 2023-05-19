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
        "priority": {"name": data['main_priority']},
        "assignee": {"name": data['main_assignee']},
        "reporter": {"name": data['main_reporter']},
        "labels": data['main_labels'],
        "customfield_10002": data['main_story_points'],  # Assuming "10002" is the custom field ID for story points
        "customfield_10003": data['main_acceptance_criteria']  # Assuming "10003" is the custom field ID for acceptance criteria
    }
}

create_ticket_url = base_url + "issue"
response = session.post(create_ticket_url, json=ticket_data)

if response.status_code == 201:
    main_ticket_key = response.json()["key"]
    print("Main ticket created successfully. Key:", main_ticket_key)
else:
    print("Failed to create main ticket:", response.text)

# Create the subtask
subtask_data = {
    "fields": {
        "project": {"key": data['project_key']},
        "parent": {"key": main_ticket_key},
        "summary": data['subtask_summary'],
        "description": data['subtask_description'],
        "issuetype": {"name": "Sub-task"},
        "priority": {"name": data['subtask_priority']},
        "assignee": {"name": data['subtask_assignee']},
        "reporter": {"name": data['subtask_reporter']},
        "labels": data['subtask_labels'],
        "customfield_10002": data['subtask_story_points'],  # Assuming "10002" is the custom field ID for story points
        "customfield_10003": data['subtask_acceptance_criteria']  # Assuming "10003" is the custom field ID for acceptance criteria
    }
}

create_subtask_url = base_url + "issue"
response = session.post(create_subtask_url, json=subtask_data)

if response.status_code == 201:
    subtask_key = response.json()["key"]
    print("Subtask created successfully. Key:", subtask_key)
else:
    print("Failed to create subtask:", response.text)
