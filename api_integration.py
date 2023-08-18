import requests
from config import JSON_URL, BASE_URL, LIST_ID

HEADERS = {
    "Content-Type": "application/json"
}

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def get_contact_lists(token, limit=1):
    headers = {**HEADERS, **get_auth_header(token)}
    response = requests.get(f"{BASE_URL}/contact_lists?limit={limit}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code} fetching contact lists: ", response.text)
        return None

def fetch_data_from_json():
    response = requests.get(JSON_URL)
    if response.status_code == 200:
        return response.json()['query_result']['data']['rows']
    else:
        print(f"Error {response.status_code} fetching data from JSON: ", response.text)
        return []

def fetch_tags_mapping(token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contact_tags"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tags_data = response.json()['tags']
        return {tag['name']: tag['tag_id'] for tag in tags_data}
    else:
        print(f"Error {response.status_code} fetching tags: ", response.text)
        return {}

def format_contact_data(contact, tags_mapping):
    """Format the contact data according to Constant Contact's expectations"""
    
    # Safely retrieve and process the Tags
    tags = contact.get('Tags', '')
    taggings = [tags_mapping[tag.strip()] for tag in tags.split(', ') if tags and tag.strip() in tags_mapping] 

    formatted = {
        'email_address': {
            'address': contact['EMAIL'],
            'permission_to_send': 'implicit'
        },
        'first_name': contact['FirstName'],
        'last_name': contact['LastName'],
        'company_name': contact['Company'],
        'update_source': 'Account',
        'phone_numbers': [{
            'phone_number': contact['Mobile'],
            'kind': 'mobile'
        }],
        'street_addresses': [{
            'kind': 'work',
            'street': contact['OfficeAddress'],
            'city': contact['OfficeCity'],
            'postal_code': contact['ZIP']
        }],
        'taggings': taggings
    }

    # Convert the Anniversary and Birthday to the expected formats
    anniversary = contact.get('Anniversary')
    if anniversary:
        anniversary_parts = anniversary.split('/')
        formatted['anniversary'] = f"{anniversary_parts[2]}-{anniversary_parts[0].zfill(2)}-{anniversary_parts[1].zfill(2)}"
    
    birthday = contact.get('Birthday')
    if birthday:
        birthday_parts = birthday.split('/')
        formatted['birthday_month'] = int(birthday_parts[0])
        formatted['birthday_day'] = int(birthday_parts[1])
    
    return formatted

def contact_exists_in_cc(email, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contacts?email={email}"
    response = requests.get(url, headers=headers)
    response_json = response.json()
    
    if response.status_code == 200:
        if "contacts" in response_json and response_json["contacts"]:
            return response_json["contacts"][0]["contact_id"]
        else:
            print(f"Unexpected response structure when checking if contact exists. Response JSON:", response_json)
            return False
    elif response.status_code == 404:
        return False
    else:
        print(f"Error {response.status_code} checking if contact exists in CC: ", response.text)
        print("Response JSON:", response_json)
        return False

def add_contact_to_list(contact_id, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contacts/{contact_id}/lists/{LIST_ID}"
    
    response = requests.put(url, headers=headers)
    if response.status_code in [200, 204]:  # Success status codes
        print(f"Successfully added contact to list: {response.json()}")
    else:
        print(f"Error {response.status_code} adding contact to list: ", response.text)

def create_contact_in_cc(contact, token, tags_mapping):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contacts"
    
    formatted_contact = format_contact_data(contact, tags_mapping)
    formatted_contact["create_source"] = "Account"
    
    response = requests.post(url, json=formatted_contact, headers=headers)
    if response.status_code == 201:
        contact_id = response.json()["contact_id"]
        print(f"Successfully created contact in CC: {response.json()}")
        #add_contact_to_list(contact_id, token)  # Add contact to list after creation
    else:
        print(f"Error {response.status_code} creating contact in CC: ", response.text)

def update_contact_in_cc(contact_id, contact, token, tags_mapping):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contacts/{contact_id}"

    formatted_contact = format_contact_data(contact, tags_mapping)
    formatted_contact["update_source"] = "Account"
    
    response = requests.put(url, json=formatted_contact, headers=headers)
    if response.status_code in [200, 204]:  # Success status codes
        print(f"Successfully updated contact in CC: {response.json()}")
        #add_contact_to_list(contact_id, token)  # Add contact to list after update
    else:
        print(f"Error {response.status_code} updating contact in CC: ", response.text)
