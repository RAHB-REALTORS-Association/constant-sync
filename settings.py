import os

# Constant Contact API settings
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'https://localhost'
AUTHORIZATION_URL = 'https://authz.constantcontact.com/oauth2/default/v1/authorize'
TOKEN_URL = 'https://authz.constantcontact.com/oauth2/default/v1/token'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'tokens.json')

# Database settings
DB_SERVER = 'hostname'
DB_NAME = 'database'
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_QUERY = 'SELECT FirstName, LastName, Email, Anniversary, Birthday, Mobile, Tags, Company, OfficeAddress, OfficeCity, ZIP, LastImport, CUST_NO, Login FROM C_Contact'
