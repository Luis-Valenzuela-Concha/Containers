# websocket_client.py
import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://websocket_server:3001" 
    async with websockets.connect(uri) as websocket:
        # Opcional: Enviar un mensaje inicial al servidor si es necesario
        await websocket.send(json.dumps({"message": "Hello, Server!"}))

        print("Conectado al servidor WebSocket. Esperando mensajes...")
        # Esperar y imprimir los mensajes recibidos del servidor
        while True:
            message = await websocket.recv()
            print(f"Recibido del servidor: {message}")

if __name__ == "__main__":
    asyncio.run(websocket_client())
