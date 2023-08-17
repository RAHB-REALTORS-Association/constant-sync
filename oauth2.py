import os
import requests
import json
from datetime import datetime, timedelta
from flask import Flask, redirect, request, render_template
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZATION_URL, TOKEN_URL

app = Flask(__name__)
app.secret_key = 'some_secret_key'

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
        'client_secret': CLIENT_SECRET
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

@app.route('/authorize')
def authorize():
    return redirect(AUTHORIZATION_URL)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=token_data)
    if response.status_code == 200:
        data = response.json()
        save_tokens_to_file(data['access_token'], data['refresh_token'], data['expires_in'])
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
