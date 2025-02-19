from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

def read_emails():
    # Load credentials from token.json
    creds = Credentials.from_authorized_user_file("gmail/token.json", ["https://www.googleapis.com/auth/gmail.readonly"])

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Fetch messages
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    # Print message IDs
    for msg in messages[:5]:  # Fetch first 5 messages
        msg_id = msg['id']
        msg_detail = service.users().messages().get(userId='me', id=msg_id).execute()
        print(f"Message ID: {msg_id}")
        print(f"Snippet: {msg_detail.get('snippet')}\n")

if __name__ == "__main__":
    read_emails()