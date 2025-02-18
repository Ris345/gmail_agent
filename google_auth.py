import os.path
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("tokens.json"):
        print("Loading credentials from token.json")
        creds = Credentials.from_authorized_user_file("tokens.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials")
            creds.refresh(Request())
        else:
            print("No valid credentials available, initiating login flow")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            flow.redirect_uri = 'http://localhost:3000/'  # Ensure this matches the authorized redirect URI
            print(f"Using redirect URI: {flow.redirect_uri}")
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            print("Saving credentials to token.json")
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        print("Building Gmail service")
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:", labels)
        for label in labels:
            print(label["name"])

    except HttpError as error:
        # TODO - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__authenticate__":
    authenticate()