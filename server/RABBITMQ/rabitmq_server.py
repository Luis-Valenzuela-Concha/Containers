import pika
import psycopg2
import os
import json
from datetime import datetime

POSTGRES_DB = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('DB_USER')
POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
POSTGRES_HOST = os.getenv('DB_HOST')

def connect():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=5432,
    )

def callback(ch, method, properties, body):
    conn = connect()
    cursor = conn.cursor()
    print(f"Received {body}")

    # Parse the JSON message
    data = json.loads(body)

    # Insert the manipulated data into the database
    cursor.execute( "INSERT INTO connections (Texto, FechaHora, Sistema, Estado) VALUES (%s, %s, %s, %s)", (data['text'], datetime.now(), data['system'], data['status']))
    conn.commit()
    cursor.close()
    conn.close()

def main():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='cola')

    # Consume messages from the queue
    channel.basic_consume(queue='cola', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()