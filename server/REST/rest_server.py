# rest_server.py
from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
import websockets
import asyncio
import json
import threading

def notify_websocket_server(data):
    asyncio.run(async_notify_websocket_server(data))

async def async_notify_websocket_server(data):
    uri = "ws://websocket_server:3001"
    async with websockets.connect(uri) as websocket:
        message = json.dumps(data)
        await websocket.send(message)

POSTGRES_DB = "mydb"
POSTGRES_USER = "myuser"
POSTGRES_PASSWORD = "mypassword"

def connect():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host='db',
        port=5432
    )

app = Flask(__name__)

@app.route('/api/message', methods=['POST'])
def post():
    data = request.get_json()
    client = data['system']
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO connections (Texto, FechaHora, Sistema, Estado) VALUES (%s, %s, %s, %s)", (data['text'], datetime.now(), client, data['status']))
    conn.commit()
    cur.execute('SELECT Count(*) AS messages_count FROM connections WHERE Sistema = %s', ('REST',))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    message_data = {
        'client': 'REST',
        'message': data['text'],
        'count': count
    }

    print(f"Message received from {message_data['client']}: {message_data['message']}")

    asyncio.run(async_notify_websocket_server(message_data))

    return jsonify(message_data)

if __name__ == '__main__':
    app.run(port=3000, host='0.0.0.0')
