import requests
from getpass import getpass

# Jira API credentials and base URL
username = input("Enter your Jira username: ")
password = getpass("Enter your Jira password: ")
base_url = "https://your-jira-instance.atlassian.net/rest/api/2/"

# Create a session
session = requests.Session()
session.auth = (username, password)

# Create the main ticket
ticket_data = {
    "fields": {
        "project": {"key": "PROJECT_KEY"},
        "summary": "Main Ticket Summary",
        "description": "Main Ticket Description",
        "issuetype": {"name": "Task"},
        "assignee": {"name": "assignee_username"},
        "reporter": {"name": "reporter_username"}
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
        "project": {"key": "PROJECT_KEY"},
        "parent": {"key": main_ticket_key},
        "summary": "Subtask Summary",
        "description": "Subtask Description",
        "issuetype": {"name": "Sub-task"},
        "assignee": {"name": "assignee_username"},
        "reporter": {"name": "reporter_username"}
    }
}

create_subtask_url = base_url + "issue"
response = session.post(create_subtask_url, json=subtask_data)

if response.status_code == 201:
    subtask_key = response.json()["key"]
    print("Subtask created successfully. Key:", subtask_key)
else:
    print("Failed to create subtask:", response.text)
