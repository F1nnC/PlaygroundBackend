import requests

# API endpoint URL
url = 'https://Playgroundproject.duckdns.org/api/users/delete_user'

# Request payload
payload = {
    'names': ['Toby' ]
}

# Send POST request
response = requests.post(url, json=payload)

# Check response status code
if response.status_code == 200:
    # Request successful
    data = response.json()
    deleted_users = data['deleted_users']
    print(f"Deleted users: {deleted_users}")
else:
    # Request failed
    print(f"Request failed with status code {response.status_code}")
