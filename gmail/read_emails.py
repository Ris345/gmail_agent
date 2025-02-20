from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import base64
import email
from datetime import datetime
import html

def read_emails():
    # Load credentials from token.json
    creds = Credentials.from_authorized_user_file("gmail/token.json", ["https://www.googleapis.com/auth/gmail.readonly"])
    
    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)
    
    # Fetch messages
    results = service.users().messages().list(userId='me', maxResults=10).execute()
    messages = results.get('messages', [])
    
    emails_data = []
    
    # Process each message
    for msg in messages:
        msg_id = msg['id']
        msg_detail = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        
        # Extract headers
        headers = msg_detail['payload']['headers']
        
        # Initialize values
        sender = subject = date = ""
        
        # Get header values
        for header in headers:
            name = header['name'].lower()
            if name == 'from':
                sender = header['value']
            elif name == 'subject':
                subject = header['value']
            elif name == 'date':
                date = header['value']
        
        # Extract message body
        body = ""
        if 'parts' in msg_detail['payload']:
            for part in msg_detail['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
        else:
            # If no parts, try to get body directly
            if 'body' in msg_detail['payload'] and 'data' in msg_detail['payload']['body']:
                body = base64.urlsafe_b64decode(msg_detail['payload']['body']['data']).decode('utf-8')
        
        # Format date
        try:
            parsed_date = email.utils.parsedate_to_datetime(date)
            formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_date = date
        
        # Add email to the collection
        emails_data.append({
            'id': msg_id,
            'sender': sender,
            'subject': subject,
            'body': body,
        })
    
    return {
        'status': 'success',
        'count': len(emails_data),
        'emails': emails_data
    }

if __name__ == "__main__":
    result = read_emails()