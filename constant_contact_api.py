import requests

class ConstantContactAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = 'https://api.cc.email/v3'

    def get_contacts(self):
        # Get all contacts in the user's account
        url = self.api_url + '/contacts'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_contact(self, data):
        # Create a new contact
        url = self.api_url + '/contacts'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['id']

    def update_contact(self, contact_id, data):
        # Update an existing contact
        url = self.api_url + '/contacts/' + contact_id
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()

    def delete_contact(self, contact_id):
        # Delete a contact
        url = self.api_url + '/contacts/' + contact_id
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
