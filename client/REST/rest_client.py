import requests
import os

REST_SERVER_PORT = os.getenv('REST_SERVER_PORT')
API_URL = 'http://rest_server:' + str(REST_SERVER_PORT) + '/'

def send_message(message):
    data = {
        'text': message,
        'system': 'REST',
        'status': True
    }
    response = requests.post(API_URL + 'api/message', json=data)
    print("Message sent: ", data)

# hace un main que reciba input muchas veces
if __name__ == '__main__':
    print("REST CLIENT IS RUNNING")
    message = ''
    while True:
        message = input('Enter a message: ')
        if message == 'exit': break
        send_message(message)
        