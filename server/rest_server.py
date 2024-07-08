from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
import os

POSTGRES_DB = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('DB_USER')
POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
REST_SERVER_PORT = os.getenv('REST_SERVER_PORT')

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
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO connections (Texto, FechaHora, Sistema, Estado) VALUES (%s, %s, %s, %s)", (data['text'], datetime.now(), data['system'], data['status']))
    conn.commit()
    cur.close()
    conn.close()
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM connections")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=REST_SERVER_PORT)
