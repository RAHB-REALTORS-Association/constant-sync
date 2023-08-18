from api_integration import fetch_data_from_json, create_contact_in_cc, contact_exists_in_cc, update_contact_in_cc
from oauth2 import get_access_token

def process_contacts_chunk(chunk):
    access_token = get_access_token()  # Ensure a valid token before processing
    if not access_token:
        print("Unable to obtain a valid access token.")
        return

    for contact in chunk:
        email = contact.get("EMAIL")
        if not email:
            print(f"Skipping contact due to missing email: {contact}")
            continue

        contact_id = contact_exists_in_cc(email, access_token)  # Pass the token to the function
        if contact_id:
            update_contact_in_cc(contact_id, contact, access_token)  # Pass the token to the function
        else:
            create_contact_in_cc(contact, access_token)  # Pass the token to the function

def synchronize_contacts():
    try:
        contacts_data = fetch_data_from_json()
        if not contacts_data:
            print("No contacts fetched from JSON.")
            return

        contacts_chunks = [contacts_data[i:i+500] for i in range(0, len(contacts_data), 500)]
        for chunk in contacts_chunks:
            process_contacts_chunk(chunk)
    except Exception as e:
        print(f"Error during synchronization: {e}")
