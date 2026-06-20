import pytest
from unittest.mock import MagicMock, patch
import base64


@pytest.fixture
def mock_service():
    service = MagicMock()
    service.users().messages().list().execute.return_value = {
        "messages": [{"id": "abc123"}]
    }

    encoded_body = base64.urlsafe_b64encode(b"Hello, this is a test email.").decode()
    service.users().messages().get().execute.return_value = {
        "payload": {
            "headers": [
                {"name": "From", "value": "sender@example.com"},
                {"name": "Subject", "value": "Test Subject"},
                {"name": "Date", "value": "Mon, 01 Jan 2024 10:00:00 +0000"},
            ],
            "body": {"data": encoded_body},
        }
    }
    return service


@patch("gmail.read_emails.Credentials")
@patch("gmail.read_emails.build")
def test_read_emails_returns_success_structure(mock_build, mock_creds, mock_service):
    mock_build.return_value = mock_service

    from gmail.read_emails import read_emails
    result = read_emails()

    assert result["status"] == "success"
    assert "emails" in result
    assert "count" in result


@patch("gmail.read_emails.Credentials")
@patch("gmail.read_emails.build")
def test_read_emails_parses_headers(mock_build, mock_creds, mock_service):
    mock_build.return_value = mock_service

    from gmail.read_emails import read_emails
    result = read_emails()

    assert result["count"] == 1
    email = result["emails"][0]
    assert email["id"] == "abc123"
    assert email["sender"] == "sender@example.com"
    assert email["subject"] == "Test Subject"


@patch("gmail.read_emails.Credentials")
@patch("gmail.read_emails.build")
def test_read_emails_empty_inbox(mock_build, mock_creds, mock_service):
    mock_service.users().messages().list().execute.return_value = {"messages": []}
    mock_build.return_value = mock_service

    from gmail.read_emails import read_emails
    result = read_emails()

    assert result["status"] == "success"
    assert result["count"] == 0
    assert result["emails"] == []


@patch("gmail.read_emails.Credentials")
@patch("gmail.read_emails.build")
def test_read_emails_decodes_multipart_body(mock_build, mock_creds, mock_service):
    encoded = base64.urlsafe_b64encode(b"Multipart body text").decode()
    mock_service.users().messages().get().execute.return_value = {
        "payload": {
            "headers": [
                {"name": "From", "value": "a@b.com"},
                {"name": "Subject", "value": "Hi"},
                {"name": "Date", "value": "Mon, 01 Jan 2024 10:00:00 +0000"},
            ],
            "parts": [
                {"mimeType": "text/plain", "body": {"data": encoded}},
                {"mimeType": "text/html", "body": {"data": encoded}},
            ],
        }
    }
    mock_build.return_value = mock_service

    from gmail.read_emails import read_emails
    result = read_emails()

    assert result["emails"][0]["body"] == "Multipart body text"
