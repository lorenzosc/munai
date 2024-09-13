import requests

def get_jwt_token(username, password):
    url = 'http://localhost:5000/login'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print(f'JWT Token: {token}')
        return token
    else:
        print(f'Failed to obtain token: {response.status_code}, {response.text}')
        return None

# Replace with your actual username and password
username = 'testuser'
password = 'testpassword'

token = get_jwt_token(username, password)
