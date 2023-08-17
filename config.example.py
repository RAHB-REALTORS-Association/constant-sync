# JSON API Endpoint
JSON_URL = "YOUR_JSON_URL_HERE"

# Constant Contact API Base URL
BASE_URL = "https://api.cc.email/v3"

# List ID for Constant Contact
LIST_ID = "YOUR_LIST_ID_HERE"

# OAuth2 Constants
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:5000/callback'  # Adjust based on where your application is hosted
AUTHORIZATION_URL = f'https://api.cc.email/v3/idfed?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}'
TOKEN_URL = 'https://idfed.constantcontact.com/as/token.oauth2'
