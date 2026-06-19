import json
import os
from pathlib import Path
from datetime import datetime
from openai import OpenAI

SPAM_DATASET = Path("data/spam_examples.jsonl")
AGENT_LOG = Path("data/agent_log.jsonl")
CONFIDENCE_THRESHOLD = float(os.getenv("SPAM_CONFIDENCE_THRESHOLD", "0.90"))


def _load_examples() -> tuple[list, list]:
    if not SPAM_DATASET.exists():
        return [], []
    examples = [json.loads(line) for line in SPAM_DATASET.read_text().splitlines() if line.strip()]
    return (
        [e for e in examples if e["label"] == "spam"],
        [e for e in examples if e["label"] == "ham"],
    )


def _classify(email: dict, spam_examples: list, ham_examples: list) -> dict:
    client = OpenAI()

    few_shot = {
        "spam": [{"sender": e["sender"], "subject": e["subject"], "body": e["body"][:200]} for e in spam_examples[:5]],
        "ham": [{"sender": e["sender"], "subject": e["subject"], "body": e["body"][:200]} for e in ham_examples[:5]],
    }

    prompt = f"""Classify this email as spam or ham using the reference examples.

Reference examples:
{json.dumps(few_shot, indent=2)}

Email to classify:
Sender: {email.get('sender', '')}
Subject: {email.get('subject', '')}
Body: {str(email.get('body', ''))[:500]}

Respond with valid JSON only:
{{"label": "spam" or "ham", "confidence": 0.0 to 1.0, "reason": "one sentence"}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content)


def _log(email: dict, result: dict, approved: bool):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "email_id": email.get("id"),
        "sender": email.get("sender"),
        "subject": email.get("subject"),
        "label": result.get("label"),
        "confidence": result.get("confidence"),
        "reason": result.get("reason"),
        "approved_for_deletion": approved,
    }
    AGENT_LOG.parent.mkdir(exist_ok=True)
    with open(AGENT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def evaluate_emails(emails: list) -> tuple[list, list]:
    """
    Classifies each email against the labeled dataset.
    Returns (approved_ids, rejected_ids).
    Only spam with confidence >= SPAM_CONFIDENCE_THRESHOLD (default 0.90) is approved.
    Errors fail safe — the email is rejected, never deleted.
    """
    spam_examples, ham_examples = _load_examples()
    approved, rejected = [], []

    for email in emails:
        email_id = email.get("id", "unknown")
        try:
            result = _classify(email, spam_examples, ham_examples)
            is_spam = result.get("label") == "spam"
            confidence = float(result.get("confidence", 0))
            approved_for_deletion = is_spam and confidence >= CONFIDENCE_THRESHOLD

            _log(email, result, approved_for_deletion)

            if approved_for_deletion:
                approved.append(email_id)
            else:
                rejected.append(email_id)
        except Exception as e:
            _log(email, {"label": "error", "confidence": 0, "reason": str(e)}, False)
            rejected.append(email_id)

    return approved, rejected
