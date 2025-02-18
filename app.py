# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, redirect, url_for
from google_auth import authenticate

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Success'

@app.route('/authorize')
def authorize():
    creds = authenticate()
    print(authenticate().token)
    return redirect(url_for('Success'))

@app.route('/retriveEmails')
def read_emails():
    print('reading email')
    

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()