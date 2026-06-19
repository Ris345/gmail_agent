from flask import Flask, redirect, url_for, jsonify, request
from gmail.google_auth import authenticate
from gmail.read_emails import read_emails, delete_emails
from Agent.parent_agent import invoke_agent


app = Flask(__name__)
invoke_agent()


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
    result = read_emails()
    return jsonify(result)


@app.route('/deleteEmails', methods=['POST'])
def delete_emails_route():
    data = request.get_json()
    email_ids = data.get('email_ids', [])
    result = delete_emails(email_ids)
    return jsonify(result)


if __name__ == '__main__':
    app.run()