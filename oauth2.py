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

            if token['expires_at'] > time.time():
                return token['access_token']

            else:
                token = self.refresh_access_token(token['refresh_token'])
                with open(self.token_file, 'w') as f:
                    json.dump(token, f)
                return token['access_token']

        else:
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
        token_data['expires_at'] = time.time() + token_data['expires_in']
        return token_data
