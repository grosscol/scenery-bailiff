from flask import Flask, jsonify, url_for, request, redirect, session, abort
from flask_login import (LoginManager, UserMixin, current_user, login_user, logout_user,
                         login_required)
from datetime import timedelta
import requests
import json
import google_auth_oauthlib.flow
from oauth2client import client
from flask_cors import CORS

# Dumb in memory users implementation
USERS = []


class User(UserMixin):
    # Use default user class provided by flask_login
    pass


CLIENT_SECRETS_FILENAME = 'client_secret.json'

# Create app
app = Flask(__name__)

# Allows ajax requests from host serving UI.
# Origin cannnot be '*' to use session cookie in requests.
CORS(app, origins=['http://localhost:8080', 'http://127.0.0.1:8080'], supports_credentials=True)

# Set the secret key to some random bytes
app.secret_key = b'exampled34db33f'

# Track logged in status via session cookie
login_manager = LoginManager()
login_manager.init_app(app)


# Dumb user lookup implementation
@login_manager.user_loader
def load_user(user_id):
    for u in USERS:
        if u.get_id() == user_id:
            user = User()
            user.id = user_id
            return user
    return None


# Create and Store User
def create_user(user_id):
    user = User()
    user.id = user_id
    USERS.append(user)
    return(user)


@app.route('/routes')
def routes():
    return '''
        <ul>
           <li><a href="/public">public<a></li>
           <li><a href="/protected">protected<a></li>
           <li><a href="/auth_status">auth_status<a></li>
           <li><a href="/authorize">authorize<a></li>
           <li><a href="/logout">logout<a></li>
        </ul>
        '''


@app.route('/public')
def public():
    data = {'data': 'public'}
    return jsonify(data)


@app.route('/protected')
@login_required
def protected():
    data = {'data': 'protected'}
    return jsonify(data)


@app.route('/accessdenied')
@login_manager.unauthorized_handler
def access_denied():
    return "Access Denied"


# Check if the current_user is authenticated and has required permissions
def is_permitted():
    if current_user.is_anonymous:
        return False
    else:
        return True


@app.route('/auth_status')
def auth_status():
    data = {}
    if current_user.is_anonymous:
        data = {'user': current_user.get_id(),
                'authenticated': current_user.is_authenticated,
                'active': current_user.is_active}
    else:
        data = {'user': current_user.get_id(),
                'authenticated': current_user.is_authenticated,
                'active': current_user.is_active}
    return jsonify(data)


# Supporting: Web server application flow
def build_authorization_url():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME,
        scopes=['https://www.googleapis.com/auth/userinfo.email'])
    flow.redirect_uri = url_for('.auth_callback', _external=True)
    return flow.authorization_url(access_type='offline', prompt='consent',
                                  include_granted_scopes='true')


# End point for starting Web server application flow
@app.route('/authorize')
def authorize():
    if current_user.is_anonymous:
        auth_url, state = build_authorization_url()
        # Store state in session as it's used to verify the returned request.
        session['state'] = state
        return redirect(auth_url)
    else:
        return auth_status()


# End point for completing Web server application flow
@app.route('/auth_callback')
def auth_callback():
    # Retrieve state from session to verify the incoming callback request
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
       CLIENT_SECRETS_FILENAME,
       scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email'],
       state=state)
    # Set same redirect uri as the initial auth request.
    flow.redirect_uri = url_for('.auth_callback', _external=True)

    # Turn around and request token from endpoint
    flow.fetch_token(authorization_response=request.url)
    # Build credentials class
    credentials = flow.credentials

    # Lookup user info endpoint from google accounts
    endpoint_resp = requests.get('https://accounts.google.com/.well-known/openid-configuration')
    endpoint_resp.raise_for_status()
    openid_endpoints = json.loads(endpoint_resp.text)
    userinfo_endpoint = openid_endpoints['userinfo_endpoint']

    # Use access token to lookup user info from google.
    user_info_resp = requests.get(userinfo_endpoint,
                                  headers={'Authorization': f'Bearer {credentials.token}'})
    user_info_resp.raise_for_status()
    userinfo = json.loads(user_info_resp.text)

    # Lookup or store user in user persistence.
    user = load_user(userinfo['email']) or create_user(userinfo['email'])

    # Use flask-login to persist login via session
    login_user(user, remember=True, duration=timedelta(hours=1))

    # Store refresh token in session to allow revoking token programatically.
    session['refresh_token'] = credentials.refresh_token

    return auth_status()


# End point for completing Server side flow.
@app.route('/auth_code', methods=['POST'])
def auth_code():
    # Get code from post data
    auth_code = request.json.get('code')

    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRETS_FILENAME, ['email'], auth_code)

    email = credentials.id_token['email']

    # Lookup or store user in user persistence.
    user = load_user(email) or create_user(email)

    # Use flask-login to persist login via session
    login_user(user, remember=True, duration=timedelta(hours=1))

    # Store refresh token in session to allow revoking token programatically.
    session['refresh_token'] = credentials.refresh_token
    return auth_status()


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return auth_status()


# Experiment with programatically revoking the acceess token of application for GDPR compliance.
@app.route('/revoke')
def revoke():
    requests.get(f'https://accounts.google.com/o/oauth2/revoke?token={session["refresh_token"]}')
    return f'Attempted Revoke using refresh token: {session["refresh_token"]}'
