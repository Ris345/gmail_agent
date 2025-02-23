from agno.agent import Agent
from agno.models.openai import OpenAIChat
import os.path
import logging
from dotenv import load_dotenv
import datetime
import requests
import time 
from apscheduler.schedulers.background import BackgroundScheduler
import time


# Define your functions
def check_mail():
    """
    Agent checks emails periodically every 2 days.
    It checks both inbox and spam, and autonomously deletes spam-related content.
    """
    # Make the API request to retrieve emails
    url = 'http://127.0.0.1:5000/retrieveEmails'
    response = requests.get(url)
    
    if response.status_code == 200:
        emails = response.json()
        return emails
    else:
        return f"Error retrieving emails: {response.status_code}"
    

def trash_cleaner():
    print("Cleaning your trash automatically!")


def remove_junk(email_ids):
    """
    After identifying junk emails, agent performs deletion to remove them.
    
    Args:
        email_ids: List of email IDs to delete
    """
    # You could implement an API call to delete the emails
    url = 'http://127.0.0.1:5000/deleteEmails'
    response = requests.post(url, json={"email_ids": email_ids})
    
    if response.status_code == 200:
        return f"Successfully deleted {len(email_ids)} junk emails"
    else:
        return f"Error deleting emails: {response.status_code}"
    

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="Email spam detection and cleanup agent",
    tools=[check_mail, remove_junk, trash_cleaner],
    show_tool_calls=True,
    markdown=True
)

agent.print_response("Look at these functions and tell me how I can make my spam cleaner successful", stream=True)


# agent gets called automatically every 3 days 
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(agent.run, 'interval', days=3)

print('scheduled successfully!',scheduler)


