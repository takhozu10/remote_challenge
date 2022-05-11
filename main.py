import requests
from dotenv import load_dotenv
import os

load_dotenv()
slack_token = os.environ['SLACK_TOKEN']
notion_token = os.environ['NOTION_TOKEN']


def get_messages():
    """Get messages from slack channel avengers-team"""
    # Configure Slack API
    slack_url = "https://slack.com/api/conversations.history"
    slack_headers = {
        "Authorization": f"{slack_token}",
    }
    slack_payload = {
        "channel": "C02MHEN44LE"
    }

    # Call API get request
    slack_response = requests.get(slack_url, params=slack_payload, headers=slack_headers).json()
    messages = slack_response["messages"]
    return messages


def insert_table(insert_date, insert_name, insert_task):
    """Insert message from slack into Notion database"""
    # Configure Notion API
    notion_url = "https://api.notion.com/v1/pages"
    notion_headers = {
        "Accept": "application/json",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
        "Authorization": f"{notion_token}"
    }
    notion_payload = {
        "parent": {
            "type": "database_id",
            "database_id": "800d8f8dddd14d6b9d87a7117da45f60"
        },
        "properties": {
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": f"{insert_name}"}}]
            },
            "Task": {
                "type": "select",
                "select": {"name": f"{insert_task}"}
            },
            "Date": {
                "type": "date",
                "date": {"start": f"{insert_date}"}
            }
        }
    }
    # Run post call to Notion database
    notion_response = requests.post(notion_url, json=notion_payload, headers=notion_headers)
    # Print message if status_code returns 200
    if notion_response.status_code == 200:
        print(f"Insert Successful: {insert_date} | {insert_name} | {insert_task}")


if __name__ == "__main__":
    # Call get_messages function to retrieve messages from Slack channel.
    slack_messages = get_messages()
    for message in slack_messages:
        # Only parse message with " | " in the messages.
        if " | " in message["text"]:
            # Split each message into a list using " | " as delimiter.
            message_split = message["text"].split(" | ")
            # Assigning each split messages to respective variables.
            # The name variable is assigned after taking "LastName, FirstName MiddleName" format, splitting into
            # [LastName, FirstName MiddleName] list using ", " as delimiter, then list is reversed by [::-1] slice notation.
            # The list is rejoined using a space " " into "FirstName MiddleName LastName" format.
            date = message_split[0]
            name = " ".join(message_split[1].split(", ")[::-1])
            task = message_split[2]
            # Call insert_table function to insert into Notion table
            insert_table(date, name, task)
