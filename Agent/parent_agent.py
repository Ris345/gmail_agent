import logging
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from evals.evaluator import evaluate_emails
import db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

AGENT_PROMPT = (
    "Check my Gmail inbox for spam and junk emails. "
    "Identify them using check_mail, then remove them using remove_junk."
)

agent = None
scheduler = None


def check_mail():
    """Fetch the last 10 inbox emails via the Flask API."""
    url = 'http://127.0.0.1:5001/retrieveEmails'
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        logger.error("check_mail: could not reach email server: %s", e)
        return f"Error reaching email server: {e}"
    if response.status_code == 200:
        return response.json()
    logger.error("check_mail: unexpected status %s", response.status_code)
    return f"Error retrieving emails: {response.status_code}"


def trash_cleaner():
    logger.info("trash_cleaner called")


def remove_junk(emails: list) -> str:
    """
    Evaluates emails for spam and deletes only confirmed spam.
    Emails that do not pass the spam eval are never deleted.

    Args:
        emails: List of email dicts with keys: id, sender, subject, body
    """
    approved_ids, rejected_ids = evaluate_emails(emails)

    logger.info(
        "remove_junk: %d approved for deletion, %d rejected",
        len(approved_ids), len(rejected_ids),
    )

    if not approved_ids:
        return "No emails passed the spam eval — nothing deleted."

    url = 'http://127.0.0.1:5001/deleteEmails'
    try:
        response = requests.post(url, json={"email_ids": approved_ids}, timeout=10)
    except requests.exceptions.RequestException as e:
        logger.error("remove_junk: could not reach email server: %s", e)
        return f"Error reaching email server: {e}"

    if response.status_code == 200:
        msg = f"Deleted {len(approved_ids)} spam emails. {len(rejected_ids)} kept (did not pass eval)."
        logger.info("remove_junk: %s", msg)
        return msg

    logger.error("remove_junk: delete request failed with status %s", response.status_code)
    return f"Error deleting emails: {response.status_code}"


def _run_agent_job():
    logger.info("Scheduler fired — starting agent run")
    try:
        agent.run(input=AGENT_PROMPT)
        logger.info("Agent run completed")
    except Exception as e:
        logger.error("Agent run failed: %s", e)


def reschedule_job(days: int):
    if scheduler is None:
        return
    if scheduler.get_job("cleanup"):
        scheduler.remove_job("cleanup")
    scheduler.add_job(
        _run_agent_job,
        "interval",
        days=days,
        id="cleanup",
    )
    logger.info("Cleanup job scheduled every %d day(s)", days)


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

    saved_days = db.get("interval_days")
    if saved_days:
        reschedule_job(int(saved_days))
        logger.info("Restored schedule from DB: every %s day(s)", saved_days)
    else:
        logger.info("No saved schedule found — set one via the UI at http://localhost:5001")
