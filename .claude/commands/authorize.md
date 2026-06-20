# Authorize Gmail

Triggers the OAuth2 flow and confirms token.json was written.

Before running, check if the scope changed since the last token was issued. If so, delete the old token first:

```bash
rm -f /Users/rishavacharya/Desktop/gmail_agent/gmail/token.json
```

Then trigger the flow (the app must already be running):

```bash
curl -v http://localhost:8080/authorize
ls -lh /Users/rishavacharya/Desktop/gmail_agent/gmail/token.json
```

After running, report:
- Whether `token.json` exists and has a recent modified time
- Whether the curl response redirected to `/` (success) or returned an error
- If auth failed, check that `credentials.json` is in the project root and the redirect URI `http://localhost:3000/` is registered in Google Cloud Console
