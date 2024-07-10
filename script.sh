#!/bin/bash

# Ejecutar el cliente REST
docker exec -it containers-rest_client-1 python rest_client.py

# Ejecutar el cliente gRPC
docker exec -it containers-grpc_client-1 python grpc_client.py

# Ejecutar el cliente RabbitMQ
docker exec -it containers-rabbitmq_client-1 python rabbitmq_client.py
