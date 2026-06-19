import pytest
from unittest.mock import patch, MagicMock
import json


SPAM_EMAIL = {"id": "s1", "sender": "prize@scam.xyz", "subject": "YOU WON!!!", "body": "Click here to claim your $5000 prize now!"}
HAM_EMAIL = {"id": "h1", "sender": "mom@gmail.com", "subject": "Dinner Sunday?", "body": "Are you free for dinner this Sunday?"}


def _mock_openai_response(label, confidence, reason="test"):
    msg = MagicMock()
    msg.content = json.dumps({"label": label, "confidence": confidence, "reason": reason})
    choice = MagicMock()
    choice.message = msg
    response = MagicMock()
    response.choices = [choice]
    return response


@patch("evals.evaluator._log")
@patch("evals.evaluator._load_examples", return_value=([], []))
@patch("evals.evaluator.OpenAI")
def test_high_confidence_spam_is_approved(mock_openai_cls, mock_load, mock_log):
    mock_openai_cls().chat.completions.create.return_value = _mock_openai_response("spam", 0.97)

    from evals.evaluator import evaluate_emails
    approved, rejected = evaluate_emails([SPAM_EMAIL])

    assert "s1" in approved
    assert rejected == []


@patch("evals.evaluator._log")
@patch("evals.evaluator._load_examples", return_value=([], []))
@patch("evals.evaluator.OpenAI")
def test_ham_email_is_rejected(mock_openai_cls, mock_load, mock_log):
    mock_openai_cls().chat.completions.create.return_value = _mock_openai_response("ham", 0.95)

    from evals.evaluator import evaluate_emails
    approved, rejected = evaluate_emails([HAM_EMAIL])

    assert approved == []
    assert "h1" in rejected


@patch("evals.evaluator._log")
@patch("evals.evaluator._load_examples", return_value=([], []))
@patch("evals.evaluator.OpenAI")
def test_low_confidence_spam_is_rejected(mock_openai_cls, mock_load, mock_log):
    mock_openai_cls().chat.completions.create.return_value = _mock_openai_response("spam", 0.75)

    from evals.evaluator import evaluate_emails
    approved, rejected = evaluate_emails([SPAM_EMAIL])

    assert approved == []
    assert "s1" in rejected


@patch("evals.evaluator._log")
@patch("evals.evaluator._load_examples", return_value=([], []))
@patch("evals.evaluator.OpenAI")
def test_openai_error_fails_safe(mock_openai_cls, mock_load, mock_log):
    mock_openai_cls().chat.completions.create.side_effect = Exception("API timeout")

    from evals.evaluator import evaluate_emails
    approved, rejected = evaluate_emails([SPAM_EMAIL])

    assert approved == []
    assert "s1" in rejected


@patch("evals.evaluator._log")
@patch("evals.evaluator._load_examples", return_value=([], []))
@patch("evals.evaluator.OpenAI")
def test_mixed_batch(mock_openai_cls, mock_load, mock_log):
    mock_openai_cls().chat.completions.create.side_effect = [
        _mock_openai_response("spam", 0.95),
        _mock_openai_response("ham", 0.99),
        _mock_openai_response("spam", 0.60),
    ]

    emails = [
        {"id": "s1", "sender": "x@spam.com", "subject": "Win!", "body": "Prize"},
        {"id": "h1", "sender": "dad@gmail.com", "subject": "Hey", "body": "Call me"},
        {"id": "s2", "sender": "y@spam.com", "subject": "Deal!", "body": "80% off"},
    ]

    from evals.evaluator import evaluate_emails
    approved, rejected = evaluate_emails(emails)

    assert approved == ["s1"]
    assert set(rejected) == {"h1", "s2"}
