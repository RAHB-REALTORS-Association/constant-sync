from constant_contact_api import ConstantContactAPI

def add_new_contact(cc_api, new_contact):
    data = {
        'email_address': new_contact['Email'],
        'first_name': new_contact['FirstName'],
        'last_name': new_contact['LastName'],
        'anniversary': new_contact['Anniversary'],
        'birthday': new_contact['Birthday'],
        'phone': new_contact['Mobile'],
        'tags': new_contact['Tags'],
        'company_name': new_contact['Company'],
        'street_address': new_contact['OfficeAddress'],
        'city': new_contact['OfficeCity'],
        'postal_code': new_contact['ZIP'],
        'custom_fields': [
            {
                'custom_field_id': 'lastimport',
                'value': new_contact['LastImport']
            },
            {
                'custom_field_id': 'login',
                'value': new_contact['Login']
            },
            {
                'custom_field_id': 'cust_no',
                'value': new_contact['CUST_NO']
            }
        ]
    }
    cc_api.add_contact(data)

def update_existing_contact(cc_api, user, contact):
    data = {
        'first_name': user['FirstName'],
        'last_name': user['LastName'],
        'anniversary': user['Anniversary'],
        'birthday': user['Birthday'],
        'phone': user['Mobile'],
        'tags': user['Tags'],
        'company_name': user['Company'],
        'street_address': user['OfficeAddress'],
        'city': user['OfficeCity'],
        'postal_code': user['ZIP'],
        'custom_fields': [
            {
                'custom_field_id': 'lastimport',
                'value': user['LastImport']
            },
            {
                'custom_field_id': 'login',
                'value': user['Login']
            },
            {
                'custom_field_id': 'cust_no',
                'value': user['CUST_NO']
            }
        ]
    }
    cc_api.update_contact(contact['id'], data)

def remove_stale_contact(cc_api, contact_id):
    cc_api.delete_contact(contact_id)

def update_contacts(new_contacts, cc_contacts):
    cc_api = ConstantContactAPI()

    # Add new contacts
    for user in new_contacts:
        if user['Email'] not in [contact['email_address'] for contact in cc_contacts]:
            add_new_contact(cc_api, user)

    # Update existing contacts
    for user in new_contacts:
        if user['Email'] in [contact['email_address'] for contact in cc_contacts]:
            contact = [contact for contact in cc_contacts if contact['email_address'] == user['Email']][0]
            update_existing_contact(cc_api, user, contact)

    # Remove stale contacts
    for contact in cc_contacts:
        if contact['email_address'] not in [user['Email'] for user in new_contacts]:
            remove_stale_contact(cc_api, contact['id'])
