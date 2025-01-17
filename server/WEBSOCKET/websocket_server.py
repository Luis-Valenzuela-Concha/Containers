import asyncio
import websockets
import psycopg2
import psycopg2.extensions
import json
import os

POSTGRES_DB = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('DB_USER')
POSTGRES_PASSWORD = os.getenv('DB_PASSWORD')
POSTGRES_HOST = os.getenv('DB_HOST')
WS_SERVER_PORT = os.getenv('WS_SERVER_PORT')

clients = set()

async def register(websocket, path):
    print("A client just connected")
    clients.add(websocket)
    try:
        async for message in websocket:
            print("Received message from client: " + message)
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        clients.remove(websocket)

async def notify_clients(tipocliente, mensaje, total):
    formatted_message = (
        f"Se ingreso un registro mediante {tipocliente}, con el mensaje {mensaje}, "
        f"total de mensajes {total}"
    )
    if clients:
        message = json.dumps({"message": formatted_message})
        await asyncio.gather(*[client.send(message) for client in clients])

async def listen_to_db():
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host='db',
                port=5432,
            )
            print("Connected to the database")
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute("LISTEN new_message;")
            break
        except Exception as e:
            retries += 1
            print(f"Exception in listen_to_db: {e}")
            await asyncio.sleep(5)
    else:
        print("Could not connect to the database")
        return
        

    while True:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            payload = json.loads(notify.payload)
            print(payload)
            tipocliente = payload.get("sistema")
            mensaje = payload.get("texto")
            total = payload.get("total")
            #print(f"Got message: {mensaje} from {tipocliente}, total messages: {total}")
            await notify_clients(tipocliente, mensaje, total)
        await asyncio.sleep(1)  # Sleep to prevent busy-waiting

if __name__ == "__main__":
    print("Starting WebSocket server")
    websocket_server = websockets.serve(register, "0.0.0.0", WS_SERVER_PORT)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websocket_server)
    loop.create_task(listen_to_db())  # Run the listen_to_db coroutine
    loop.run_forever()