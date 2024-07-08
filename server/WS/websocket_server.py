# websocket_server.py
import asyncio
import websockets

connected_clients = set()

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def send_message(message):
    if connected_clients:  # Verifica si hay clientes conectados
        await asyncio.wait([client.send(message) for client in connected_clients])

async def main():
    async with websockets.serve(handler, "0.0.0.0", 6789):
        print("WebSocket Server started at ws://0.0.0.0:6789")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    print("Starting WebSocket Server")
    asyncio.run(main())
