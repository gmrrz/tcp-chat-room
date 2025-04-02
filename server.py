import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket, path):
    # Registering client
    connected_clients.add(websocket)
    print(f"Client connected {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Recieved from client: {message}")
            # Projet the message to all clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(f"User: {message}")

    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        # Unregister Client
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8080):
        print("WebSocket server is running on ws://0.0.0.0:8080")
        await asyncio.Future() # Runs forever

    asyncio.run(main())