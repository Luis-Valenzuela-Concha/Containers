import asyncio
import websockets
import json
import os

WS_SERVER_PORT = os.getenv('WS_SERVER_PORT')

async def listen():
    url = "ws://websocket_server:" + str(WS_SERVER_PORT)
    async with websockets.connect(url) as ws:
        await ws.send("Hello Server!")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)  # Parsear el JSON recibido
            message = data.get("message")  # Obtener el valor del campo 'message'
            if message:
                print(message)  # Imprimir solo el contenido del campo 'message'

asyncio.get_event_loop().run_until_complete(listen())