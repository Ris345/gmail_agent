from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from evals.evaluator import evaluate_emails


# Define your functions
def check_mail():
    """
    Agent checks emails periodically every 2 days.
    It checks both inbox and spam, and autonomously deletes spam-related content.
    """
    # Make the API request to retrieve emails
    url = 'http://127.0.0.1:5000/retrieveEmails'
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        return f"Error reaching email server: {e}"
    if response.status_code == 200:
        return response.json()
    return f"Error retrieving emails: {response.status_code}"
    

def trash_cleaner():
    print("Cleaning your trash automatically!")


def remove_junk(emails: list) -> str:
    """
    Evaluates emails for spam and deletes only confirmed spam.
    Emails that do not pass the spam eval are never deleted.

    Args:
        emails: List of email dicts with keys: id, sender, subject, body
                (as returned by check_mail)
    """
    approved_ids, rejected_ids = evaluate_emails(emails)

    if rejected_ids:
        print(f"Eval rejected {len(rejected_ids)} emails (not confident enough to delete): {rejected_ids}")

    if not approved_ids:
        return "No emails passed the spam eval — nothing deleted."

    url = 'http://127.0.0.1:5000/deleteEmails'
    try:
        response = requests.post(url, json={"email_ids": approved_ids}, timeout=10)
    except requests.exceptions.RequestException as e:
        return f"Error reaching email server: {e}"
    if response.status_code == 200:
        return f"Deleted {len(approved_ids)} spam emails. {len(rejected_ids)} emails were kept (did not pass eval)."
    return f"Error deleting emails: {response.status_code}"
    

agent = None
scheduler = None


def invoke_agent():
    global agent, scheduler
    load_dotenv()

    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        description="Email spam detection and cleanup agent",
        tools=[check_mail, remove_junk, trash_cleaner],
        markdown=True,
    )

    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        agent.run,
        "interval",
        days=3,
        kwargs={"message": "Check my Gmail inbox for spam and junk emails. Identify them using check_mail, then remove them using remove_junk."},
    )
    print("scheduled successfully!", scheduler)


