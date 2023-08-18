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

def fetch_all_cc_contacts(token):
    all_contacts = []
    page = 1
    page_size = 500
    
    while True:
        headers = {**HEADERS, **get_auth_header(token)}
        url = f"{BASE_URL}/contacts?limit={page_size}&page={page}"
        response = requests.get(url, headers=headers)
        response_json = response.json()

        if response.status_code == 200:
            contacts = response_json.get("contacts", [])
            if not contacts:
                break
            all_contacts.extend(contacts)
            page += 1
        else:
            print(f"Error {response.status_code} fetching contacts page {page} from CC: ", response.text)
            break

    return all_contacts

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
    formatted = {
        'email_address': {
            'address': contact['EMAIL'],
            'permission_to_send': 'implicit'
        },
        'first_name': contact.get('FirstName', ''),
        'last_name': contact.get('LastName', ''),
        'company_name': contact.get('Company', ''),
        'update_source': 'Account',
        'phone_numbers': [{
            'phone_number': contact.get('Mobile', ''),
            'kind': 'mobile'
        }],
        'street_addresses': [{
            'kind': 'work',
            'street': contact.get('OfficeAddress', ''),
            'city': contact.get('OfficeCity', ''),
            'postal_code': contact.get('ZIP', '')
        }],
        'taggings': [tags_mapping[tag.strip()] for tag in contact.get('Tags', '').split(', ') if tag.strip() in tags_mapping]
    }

    if 'Anniversary' in contact:
        anniversary_parts = contact['Anniversary'].split('/')
        formatted['anniversary'] = f"{anniversary_parts[2]}-{anniversary_parts[0].zfill(2)}-{anniversary_parts[1].zfill(2)}"
    
    if 'Birthday' in contact:
        birthday_parts = contact['Birthday'].split('/')
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
            return False
    elif response.status_code == 404:
        return False
    else:
        print(f"Error {response.status_code} checking if contact exists in CC: ", response.text)
        return False

def bulk_import_in_cc(contacts, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/activities/contacts"
    response = requests.post(url, json=contacts, headers=headers)
    if response.status_code == 202:
        return response.json()["activity_id"]
    else:
        print(f"Error {response.status_code} during bulk import in CC: ", response.text)
        return None

def bulk_delete_in_cc(contact_ids, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/activities/contact_delete"
    data = {
        "contact_ids": contact_ids
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 202:
        return response.json()["activity_id"]
    else:
        print(f"Error {response.status_code} during bulk delete in CC: ", response.text)
        return None

def check_activity_status(activity_id, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/activities/{activity_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["status"]
    else:
        print(f"Error {response.status_code} checking activity status in CC: ", response.text)
        return None
