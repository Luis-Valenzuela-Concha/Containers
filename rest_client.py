import requests
import time

API_URL = 'http://localhost:3000/'
    
def get_db():
    try:
        response = requests.get(API_URL + 'db')
        if response.status_code == 200:
            print(response.text)
        else:
            print('Error:', response.status_code)
    except requests.exceptions.ConnectionError as e:
        print('Connection error...')


if __name__ == '__main__':
    get_db()