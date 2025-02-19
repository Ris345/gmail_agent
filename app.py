from flask import Flask, redirect, url_for
from gmail.google_auth import authenticate
from gmail.read_emails import read_emails

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Success'

@app.route('/authorize')
def authorize():
    creds = authenticate()
    if creds: 
        print('authentication successful, now checking mails')
        read_emails()
    return redirect(url_for('hello_world'))

@app.route('/retrieveEmails', methods=['GET'])
def emails():
    read_emails()
    print('reading email')
    return 'Emails retrieved'

if __name__ == '__main__':
    app.run()