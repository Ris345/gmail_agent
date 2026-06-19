import pytest
from unittest.mock import patch, MagicMock
from Agent.parent_agent import check_mail, remove_junk


@patch("requests.get")
def test_check_mail_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "count": 1,
        "emails": [{"id": "x1", "sender": "a@b.com", "subject": "Hey", "body": ""}],
    }
    mock_get.return_value = mock_response

    result = check_mail()

    assert result["status"] == "success"
    assert result["count"] == 1


@patch("requests.get")
def test_check_mail_api_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = check_mail()

    assert "Error" in result


EMAILS = [
    {"id": "id1", "sender": "scam@win.xyz", "subject": "You won!", "body": "Claim your prize"},
    {"id": "id2", "sender": "phish@bank.fake", "subject": "Verify account", "body": "Click here now"},
]


@patch("requests.post")
@patch("Agent.parent_agent.evaluate_emails", return_value=(["id1", "id2"], []))
def test_remove_junk_success(mock_eval, mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = remove_junk(EMAILS)

    assert "Deleted 2" in result


@patch("requests.post")
@patch("Agent.parent_agent.evaluate_emails", return_value=(["id1"], []))
def test_remove_junk_api_error(mock_eval, mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_post.return_value = mock_response

    result = remove_junk(EMAILS[:1])

    assert "Error" in result


@patch("Agent.parent_agent.evaluate_emails", return_value=([], ["id1", "id2"]))
def test_remove_junk_all_rejected_by_eval(mock_eval):
    result = remove_junk(EMAILS)

    assert "No emails passed" in result
