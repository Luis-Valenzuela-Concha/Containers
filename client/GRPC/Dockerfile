# Use the official Python image from the Docker Hub
FROM python:3.9-slim

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copia todos los scripts necesarios
COPY . /app

WORKDIR /app

# Specify the command to run the gRPC client
CMD ["python", "-u", "grpc_client.py"]