import pika
import json

def send_message(message):
    # Format the message into a JSON string
    data = {
        'text': message,
        'system': 'RABBITMQ',
        'status': True
    }
    json_message = json.dumps(data)

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='cola')

    # Send a message
    channel.basic_publish(exchange='', routing_key='cola', body=json_message)
    print(f"Sent {json_message}")

    # Close the connection
    connection.close()

# hace un main que reciba input muchas veces
if __name__ == '__main__':
    print("RABBITMQ CLIENT IS RUNNING")
    message = ''
    while True:
        message = input('Enter a message: ')
        if message == 'exit': break
        send_message(message)