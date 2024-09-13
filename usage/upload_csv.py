import requests

def upload_csv_file(token, csv_file_path):
    url = 'http://localhost:5000/upload-csv'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    with open(csv_file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        print('CSV file uploaded successfully')
        print(response.json())
    else:
        print(f'Failed to upload CSV file: {response.status_code}, {response.text}')

# Replace with the JWT token you obtained
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNjIzMzA4NCwianRpIjoiMWIwNzBiZWEtZjhkOS00NjBhLTgyZDMtMDdmMDVmMWM3NTFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3R1c2VyIiwibmJmIjoxNzI2MjMzMDg0LCJjc3JmIjoiNTRhMzllYzktMmRjZi00OGVkLWFmMjAtM2UzNmFhZjZmMzcxIiwiZXhwIjoxNzI2MzE5NDg0fQ.x2Q2iMOzn-H7ZVn2EYZBKUOgUT7TCpWv0n_TVsbKhMk'

# Replace with the path to your CSV file
csv_file_path = 'patients.csv'

upload_csv_file(token, csv_file_path)
