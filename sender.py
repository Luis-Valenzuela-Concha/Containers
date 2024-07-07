import argparse
from client import rest_client, rabbitmq_client, grpc_client

parser = argparse.ArgumentParser(description='Execute another script with two string arguments.')
parser.add_argument('arg1', help='First string argument')
parser.add_argument('arg2', help='Second string argument')

args = parser.parse_args()

if args.arg1 == "REST":
    rest_client.send_message(args.arg2)
elif args.arg1 == "RABBITMQ":
    rabbitmq_client.send_message(args.arg2)
elif args.arg1 == "GRPC":
    grpc_client.send_message(args.arg2)
else:
    print("Invalid argument. Please provide either REST, RABBITMQ or GRPC.")
    