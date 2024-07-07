from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2


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

@app.route('/db', methods=['GET'])
def get_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM connections;')
    rows = cur.fetchall()
    conn.close()
    return jsonify({'rows': rows})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
