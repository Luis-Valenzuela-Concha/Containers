# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Instala todas las dependencias necesarias para los clientes y servidores
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copia todos los scripts necesarios
COPY . /app

WORKDIR /app

# Set the entry point for the container
CMD ["python", "-u", "rest_client.py"]