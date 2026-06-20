import pytest
from unittest.mock import patch
import app as flask_app


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


def test_index_returns_success(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Gmail Agent" in response.data


@patch("app.read_emails")
def test_retrieve_emails_returns_json(mock_read, client):
    mock_read.return_value = {
        "status": "success",
        "count": 2,
        "emails": [
            {"id": "1", "sender": "a@b.com", "subject": "Hello", "body": "Hi"},
            {"id": "2", "sender": "c@d.com", "subject": "World", "body": "Bye"},
        ],
    }

    response = client.get("/retrieveEmails")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] == 2
    assert len(data["emails"]) == 2


@patch("app.read_emails")
def test_retrieve_emails_empty(mock_read, client):
    mock_read.return_value = {"status": "success", "count": 0, "emails": []}

    response = client.get("/retrieveEmails")

    assert response.status_code == 200
    assert response.get_json()["count"] == 0
