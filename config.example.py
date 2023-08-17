# JSON API Endpoint
JSON_URL = "YOUR_JSON_URL_HERE"

# Constant Contact API Base URL
BASE_URL = "https://api.cc.email/v3"

# List ID for Constant Contact
LIST_ID = "YOUR_LIST_ID_HERE"

# OAuth2 Constants
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'  # Adjust based on where your application is hosted
AUTHORIZATION_URL = f'https://authz.constantcontact.com/oauth2/default/v1/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
TOKEN_URL = 'https://authz.constantcontact.com/oauth2/default/v1/token'
