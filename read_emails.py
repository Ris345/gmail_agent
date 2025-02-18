from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Load credentials from token
creds = Credentials(token="")  # Replace with your token

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



