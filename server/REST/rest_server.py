from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
import os

# POSTGRES_DB = os.getenv('DB_NAME')
# POSTGRES_USER = os.getenv('DB_USER')
# POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
# POSTGRES_HOST = os.getenv('DB_HOST')
# REST_SERVER_PORT = os.getenv('REST_SERVER_PORT')

DB_PASSWORD= "mypassword"
DB_USER= "myuser"
DB_NAME= "mydb"
DB_HOST = "db"

POSTGRES_DB = DB_NAME
POSTGRES_USER = DB_USER
POSTGRES_PASSWORD = DB_PASSWORD
POSTGRES_HOST = DB_HOST
REST_SERVER_PORT = 3000


def connect():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=5432,
    )

app = Flask(__name__)

@app.route('/api/message', methods=['POST'])
def post():
    date = datetime.now()
    data = request.get_json()
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO connections (Texto, FechaHora, Sistema, Estado) VALUES (%s, %s, %s, %s)", (data['text'], date, data['system'], data['status']))
    conn.commit()
    cur.close()
    conn.close()

    data = {
        'text': data['text'],
        'date': date,
        'system': data['system'],
        'status': data['status']
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=REST_SERVER_PORT)
