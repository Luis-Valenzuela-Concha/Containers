import requests

API_URL = 'http://rest_server:3000/'

def send_message(message):
    data = {
        'text': message,
        'system': 'REST',
        'status': True
    }
    response = requests.post(API_URL + 'api/message', json=data)
    print("Message sent: ", response.json())

# hace un main que reciba input muchas veces
if __name__ == '__main__':
    print("REST CLIENT IS RUNNING")
    message = ''
    while True:
        message = input('Enter a message: ')
        if message == 'exit': break
        send_message(message)
        