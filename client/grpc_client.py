import grpc
import message_pb2
import message_pb2_grpc

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