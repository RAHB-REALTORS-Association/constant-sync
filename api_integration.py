import requests
from config import JSON_URL, BASE_URL, LIST_ID

HEADERS = {
    "Content-Type": "application/json"
}

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def fetch_data_from_json():
    response = requests.get(JSON_URL)
    if response.status_code == 200:
        return response.json()['query_result']['data']['rows']
    else:
        print(f"Error {response.status_code} fetching data from JSON: ", response.text)
        return []

def contact_exists_in_cc(email, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contacts?email={email}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.json()["results"]:
        return response.json()["results"][0]["contact_id"]
    elif response.status_code == 404:
        return False
    else:
        print(f"Error {response.status_code} checking if contact exists in CC: ", response.text)
        return False

def create_contact_in_cc(contact, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contacts"
    contact["lists"] = [{"id": LIST_ID}]
    response = requests.post(url, json=contact, headers=headers)
    if response.status_code != 201:
        print(f"Error {response.status_code} creating contact in CC: ", response.text)

def update_contact_in_cc(contact_id, contact, token):
    headers = {**HEADERS, **get_auth_header(token)}
    url = f"{BASE_URL}/contacts/{contact_id}"
    contact["lists"] = [{"id": LIST_ID}]
    response = requests.put(url, json=contact, headers=headers)
    if response.status_code != 204:
        print(f"Error {response.status_code} updating contact in CC: ", response.text)
