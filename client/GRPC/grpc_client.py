import grpc
import sys
import os
from proto import message_pb2
from proto import message_pb2_grpc

# back to current_dir
sys.path.pop(0)

GRPC_SERVER_URL = 'grpc_server:50051'

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

# hace un main que reciba input muchas veces
if __name__ == '__main__':
    print("GRPC CLIENT IS RUNNING")
    message = ''
    while True:
        message = input('Enter a message: ')
        if message == 'exit': break
        send_message(message)