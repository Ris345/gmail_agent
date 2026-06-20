from flask import Flask, redirect, url_for, jsonify, request, render_template
from gmail.google_auth import authenticate
from gmail.read_emails import read_emails, delete_emails
from Agent.parent_agent import invoke_agent, reschedule_job
import db
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
invoke_agent()


@app.route('/')
def index():
    authorized = os.path.exists("gmail/token.json")
    schedule = db.get("interval_days")
    message = request.args.get("message")
    message_type = request.args.get("message_type", "success")
    return render_template(
        "index.html",
        authorized=authorized,
        schedule=schedule,
        message=message,
        message_type=message_type,
    )


@app.route('/authorize')
def authorize():
    creds = authenticate()
    if creds:
        read_emails()
    return redirect(url_for('index', message="Gmail connected successfully.", message_type="success"))


@app.route('/schedule', methods=['POST'])
def schedule():
    days = request.form.get('days', type=int)
    if not days or not (1 <= days <= 7):
        return redirect(url_for('index', message="Invalid interval. Choose 1–7 days.", message_type="error"))
    db.set("interval_days", days)
    reschedule_job(days)
    return redirect(url_for('index', message=f"Cleanup scheduled every {days} day{'s' if days > 1 else ''}.", message_type="success"))


@app.route('/retrieveEmails', methods=['GET'])
def emails():
    result = read_emails()
    return jsonify(result)


@app.route('/deleteEmails', methods=['POST'])
def delete_emails_route():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400
    email_ids = data.get('email_ids', [])
    result = delete_emails(email_ids)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
