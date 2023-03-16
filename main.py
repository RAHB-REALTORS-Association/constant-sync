import json
import settings
from oauth2 import OAuth2Handler
from database import Database
from constant_contact_api import ConstantContactAPI
from update_contacts import update_contacts

DB_SERVER = settings.DB_SERVER
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_QUERY = settings.DB_QUERY

def main():
    # Authenticate and obtain access token
    oauth2 = OAuth2Handler()
    access_token = oauth2.get_access_token()

    # Initialize the Constant Contact API
    cc_api = ConstantContactAPI(access_token)

    # Initialize the database and get the contacts
    db = Database(DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_QUERY)
    new_contacts = db.get_contacts()

    # Get the contacts from Constant Contact
    cc_contacts = cc_api.get_contacts()

    # Update the contacts in Constant Contact
    update_contacts(new_contacts, cc_contacts)

if __name__ == '__main__':
    main()
