import requests
import time

API_URL = 'http://localhost:3000/'

def send_message(message):
    data = {
        'text': message,
        'system': 'REST',
        'status': True
    }
    response = requests.post(API_URL + 'api/message', json=data)
    print(response.json())
