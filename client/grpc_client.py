import grpc
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)  # Subir un nivel
sys.path.insert(0, parent_dir)

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