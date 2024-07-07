import asyncio
import websockets
import psycopg2
import psycopg2.extensions
import json

POSTGRES_DB = "mydb"
POSTGRES_USER = "myuser"
POSTGRES_PASSWORD = "mypassword"

clients = set()

async def register(websocket):
    clients.add(websocket)
    try:
        await websocket.waitclosed()
    finally:
        clients.remove(websocket)

async def notify_clients(message):
    if clients:
        message = json.dumps({"message": message})
        await asyncio.wait([client.send(message) for client in clients])

async def listen_to_db():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host='db',
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("LISTEN new_message;")

    while True:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            message = notify.payload
            await notify_clients(message)

async def main():
    websocket_server = websockets.serve(register, "0.0.0.0", 8765)
    await asyncio.gather(websocket_server, listen_to_db())

if __name__ == "__main__":
    print("Websocket server running")
    asyncio.run(main())