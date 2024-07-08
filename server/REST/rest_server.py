from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
import websockets
import asyncio
import json

async def notify_websocket_server(data):
    uri = "ws://websocket_server:6789"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(data))

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
    cur.close()
    conn.close()

    message_data = {
        'client': 'REST',
        'message': data['text'],
        'status': data['status']
    }

    asyncio.run(notify_websocket_server(message_data))
    
    return jsonify(message_data)

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
