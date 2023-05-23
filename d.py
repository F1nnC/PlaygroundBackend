import requests

# API endpoint URL
url = 'https://Playgroundproject.duckdns.org/api/users/delete_user/101'

# Request payload
payload = {
    'names': ['Gene']
}

# Send DELETE request
response = requests.delete(url, json=payload)

# Check response status code
if response.status_code == 200:
    # Request successful
    data = response.json()
    deleted_users = data['deleted_users']
else:
    # Request failed
    print(f"Request failed with status code {response.status_code}")
