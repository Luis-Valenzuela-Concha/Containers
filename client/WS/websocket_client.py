# websocket_client.py
import asyncio
import websockets

async def listen():
    uri = "ws://websocket_server:6789"
    async with websockets.connect(uri) as websocket:
        print(f"Connected to WebSocket server at {uri}")
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

if __name__ == "__main__":
    print("Starting WebSocket Client")
    asyncio.get_event_loop().run_until_complete(listen())
