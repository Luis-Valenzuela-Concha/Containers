FROM python:3.8-slim

# Instala todas las dependencias necesarias para los clientes y servidores
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Copia todos los scripts necesarios
COPY . /app

COPY ./proto ./app/client/
COPY ./proto ./app/server/

WORKDIR /app

CMD ["bash"]