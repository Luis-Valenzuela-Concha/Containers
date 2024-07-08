FROM python:3.8-slim

# Copiar el script sender.py (y cualquier otro archivo necesario) al contenedor
COPY sender.py ./
COPY client/ client/

RUN pip install --no-cache-dir requests

CMD ["bash"]

