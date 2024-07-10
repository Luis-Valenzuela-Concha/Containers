import grpc
import sys
import os
from proto import message_pb2
from proto import message_pb2_grpc

# back to current_dir
sys.path.pop(0)

GRPC_PORT = os.getenv('GRPC_SERVER_PORT')
GRPC_SERVER_URL = 'grpc_server:' + GRPC_PORT

def send_message(message):
    data = {
        'text': message,
        'system': 'GRPC',
        'status': True
    }
    with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
        stub = message_pb2_grpc.MessageServiceStub(channel)
        response = stub.SendMessage(
            message_pb2.MessageRequest(
                text=data['text'],
                system=data['system'],
                status=data['status']
            )
        )
        print("Message sent: ", data)

# hace un main que reciba input muchas veces
if __name__ == '__main__':
    print("GRPC CLIENT IS RUNNING")
    message = ''
    while True:
        message = input('Enter a message: ')
        if message == 'exit': break
        send_message(message)