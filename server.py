import asyncio
import websockets

async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 8080)
    print("WebSocket server running on ws://0.0.0.0:8080")

    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("Shutting down the server...")
        server.close()
        await server.wait_closed()  # Gracefully close the server

async def handle_client(websocket, path):
    print("Handling client...")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
