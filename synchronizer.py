import time
from api_integration import (
    fetch_data_from_json, fetch_tags_mapping, fetch_all_cc_contacts, format_contact_data, 
    bulk_import_in_cc, bulk_delete_in_cc, check_activity_status
)
from oauth2 import get_access_token

def categorize_contacts(json_contacts, cc_contacts):
    # Convert contact lists to dictionaries with email as the key for efficient lookup
    json_dict = {contact['EMAIL']: contact for contact in json_contacts}
    cc_dict = {contact['email_address']['address']: contact for contact in cc_contacts}

    # Using set operations to find unique and shared contacts
    json_emails = set(json_dict.keys())
    cc_emails = set(cc_dict.keys())

    to_add_emails = json_emails - cc_emails
    to_remove_emails = cc_emails - json_emails
    shared_emails = json_emails.intersection(cc_emails)

    # Populate lists with contacts based on the emails found above
    to_add = [json_dict[email] for email in to_add_emails]
    to_remove = [cc_dict[email] for email in to_remove_emails]

    # For shared contacts, we will check each field to determine if an update is needed
    to_update = []
    for email in shared_emails:
        json_contact = json_dict[email]
        cc_contact = cc_dict[email]
        if json_contact != cc_contact:
            to_update.append(json_contact)

    return to_add, to_remove, to_update

def synchronize_contacts():
    try:
        contacts_data = fetch_data_from_json()
        if not contacts_data:
            print("No contacts fetched from JSON.")
            return

        access_token = get_access_token()
        if not access_token:
            print("Unable to obtain a valid access token.")
            return

        # Fetch the tags mapping from Constant Contact
        tags_mapping = fetch_tags_mapping(access_token)

        cc_contacts = fetch_all_cc_contacts(access_token)
        to_add, to_remove, to_update = categorize_contacts(contacts_data, cc_contacts)

        # Prepare the contacts for bulk import
        formatted_to_add = [format_contact_data(contact, tags_mapping) for contact in to_add]
        formatted_to_update = [format_contact_data(contact, tags_mapping) for contact in to_update]

        # Start the bulk import process for additions and updates
        all_contacts = formatted_to_add + formatted_to_update
        if all_contacts:
            activity_id = bulk_import_in_cc(all_contacts, access_token)
            if activity_id:
                # We can check the status of the activity until it's complete
                while True:
                    status = check_activity_status(activity_id, access_token)
                    if status == "COMPLETE":
                        break
                    time.sleep(5)  # Check every 5 seconds

        # Start the bulk delete process
        if to_remove:
            contact_ids_to_remove = [contact['contact_id'] for contact in to_remove]
            activity_id = bulk_delete_in_cc(contact_ids_to_remove, access_token)
            if activity_id:
                # We can check the status of the activity until it's complete
                while True:
                    status = check_activity_status(activity_id, access_token)
                    if status == "COMPLETE":
                        break
                    time.sleep(5)  # Check every 5 seconds

    except Exception as e:
        print(f"Error during synchronization: {e}")
