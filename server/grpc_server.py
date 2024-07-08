import grpc
from concurrent import futures
import time
import datetime  # Importa datetime para obtener la hora actual
import message_pb2
import message_pb2_grpc
import psycopg2
import os

POSTGRES_DB = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('DB_USER')
POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
REST_SERVER_PORT = os.getenv('REST_SERVER_PORT')

class MessageService(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def SendMessage(self, request, context):
        # Accede a los campos del mensaje directamente
        text = request.text
        system = request.system
        status = request.status
        try:
            cursor = self.db_connection.cursor()
            # Usa datetime.datetime.now() para obtener la hora actual
            cursor.execute("INSERT INTO connections (Texto, FechaHora, Sistema, Estado) VALUES (%s, %s, %s, %s)", (text, datetime.datetime.now(), system, status))
            self.db_connection.commit()
            cursor.close()
            return message_pb2.MessageResponse(status="Message received and stored in DB")
        except Exception as e:
            print(f"Error: {e}")
            # Usa context para indicar un error
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error storing message in DB')
            return message_pb2.MessageResponse(status="Error storing message in DB")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:    
            db_connection = psycopg2.connect(
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host="db",
                port=5432
            )
            message_pb2_grpc.add_MessageServiceServicer_to_server(MessageService(db_connection), server)
            server.add_insecure_port('[::]:50051')
            server.start()
            break
        except Exception as e:
            print(f"Error: {e}")
            retries += 1
            time.sleep(5)
            continue
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()