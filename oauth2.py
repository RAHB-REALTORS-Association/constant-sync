import json
import os
import time
import requests
from settings import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_URL, TOKEN_URL, TOKEN_FILE

class OAuth2Handler:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.authorization_url = AUTHORIZATION_URL
        self.token_url = TOKEN_URL
        self.token_file = TOKEN_FILE

    def get_access_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                token = json.load(f)

            if token['expires_at'] > time.time() and 'access_token' in token:
                return token['access_token']

            elif 'refresh_token' in token:
                new_token = self.refresh_access_token(token['refresh_token'])
                if 'access_token' in new_token:
                    with open(self.token_file, 'w') as f:
                        json.dump(new_token, f)
                    return new_token['access_token']
                else:
                    print("Refresh token is invalid or expired. Please reauthorize the application.")
                    os.remove(self.token_file)
            else:
                print("Refresh token not found. Please reauthorize the application.")
                os.remove(self.token_file)

        # If the token file does not exist or has been removed due to errors, request a new access token
        code_request = f"{self.authorization_url}?response_type=code&client_id={self.client_id}&scope=contact_data&access_type=offline&redirect_uri=https://localhost&state=randomstate"
        print(f"Please go to this URL and authorize the application: {code_request}")
        callback_url = input("Enter the full callback URL: ")

        code = self.parse_code(callback_url)
        token = self.request_access_token(code)

        with open(self.token_file, 'w') as f:
            json.dump(token, f)

        return token['access_token']

    def parse_code(self, callback_url):
        query = callback_url.split('?')[1]
        params = query.split('&')
        for param in params:
            key, value = param.split('=')
            if key == 'code':
                return value
        return None

    def request_access_token(self, code):
        token_request_data = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://localhost"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(self.token_url, auth=(self.client_id, self.client_secret), headers=headers, data=token_request_data)
        token_data = response.json()
        token_data['expires_at'] = time.time() + token_data['expires_in']
        return token_data

    def refresh_access_token(self, refresh_token):
        token_request_data = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(self.token_url, auth=(self.client_id, self.client_secret), headers=headers, data=token_request_data)
        token_data = response.json()
        
        if 'expires_in' in token_data:
            token_data['expires_at'] = time.time() + token_data['expires_in']
        else:
            # handle missing 'expires_in' here, e.g., set a default value or log a warning
            token_data['expires_at'] = time.time() + 86400

        return token_data
