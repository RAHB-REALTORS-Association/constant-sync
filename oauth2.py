import os
import requests
import json
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, redirect, request, render_template, session
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZATION_URL, TOKEN_URL
from synchronizer import synchronize_contacts

oauth2_blueprint = Blueprint('oauth2', __name__)

TOKEN_FILE = 'tokens.json'

def ensure_token_file_exists():
    if not os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "w") as file:
            json.dump({
                "access_token": "",
                "refresh_token": "",
                "expires_in": 0
            }, file)

# Call this function at the beginning to ensure tokens.json exists
ensure_token_file_exists()

def save_tokens_to_file(access_token, refresh_token, expires_in):
    expiration_time = datetime.now() + timedelta(seconds=expires_in)
    token_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_at': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(TOKEN_FILE, 'w') as f:
        json.dump(token_data, f)

def load_tokens_from_file():
    try:
        with open(TOKEN_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def is_token_expired(token_data):
    expires_at = datetime.strptime(token_data['expires_at'], '%Y-%m-%d %H:%M:%S')
    return datetime.now() > expires_at - timedelta(minutes=5)  # Buffer of 5 minutes

def refresh_access_token():
    token_data = load_tokens_from_file()
    refresh_token = token_data.get('refresh_token')
    
    if not refresh_token:
        return None

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'contact_data'
    }
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        new_tokens = response.json()
        save_tokens_to_file(new_tokens['access_token'], new_tokens['refresh_token'], new_tokens['expires_in'])
        return new_tokens['access_token']
    else:
        handle_error(response)
        return None

def get_access_token():
    token_data = load_tokens_from_file()
    if not token_data:
        return None
    
    if is_token_expired(token_data):
        return refresh_access_token()
    else:
        return token_data.get('access_token')

@oauth2_blueprint.route('/authorize')
def authorize():
    # Generate a unique state value
    state = secrets.token_urlsafe(16)
    session['state'] = state  # Save state value in the user's session
    
    # Append the scope and state to the authorization URL
    url_with_scope_and_state = f"{AUTHORIZATION_URL}&scope=contact_data&state={state}"
    return redirect(url_with_scope_and_state)

@oauth2_blueprint.route('/callback')
def callback():
    code = request.args.get('code')
    returned_state = request.args.get('state')
    
    # Validate the state value
    if 'state' not in session or session['state'] != returned_state:
        return render_template('error.html', error_message="State validation failed.")

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'contact_data'
    }
    response = requests.post(TOKEN_URL, data=token_data)
    if response.status_code == 200:
        data = response.json()
        save_tokens_to_file(data['access_token'], data.get('refresh_token', ''), data['expires_in'])
        
        # Trigger synchronization immediately after a successful authorization
        synchronize_contacts()

        return render_template('success.html')
    else:
        handle_error(response)
        return render_template('error.html', error_message=f"Error during authorization: {response.text}")

def handle_error(response):
    if response.status_code == 400:
        # Handle "Bad Request" error
        print("Error 400: Bad Request - ", response.text)
    elif response.status_code == 401:
        # Handle "Unauthorized" error
        print("Error 401: Unauthorized - ", response.text)
        # Ideally, you'd trigger a token refresh here if it's an auth error.
    elif response.status_code == 403:
        # Handle "Forbidden" error
        print("Error 403: Forbidden - ", response.text)
    elif response.status_code == 404:
        # Handle "Not Found" error
        print("Error 404: Not Found - ", response.text)
    elif response.status_code == 500:
        # Handle "Internal Server Error"
        print("Error 500: Internal Server Error - ", response.text)
    else:
        print(f"Error {response.status_code}: ", response.text)
