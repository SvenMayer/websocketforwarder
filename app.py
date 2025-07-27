# -*- coding: utf-8 -*-
import asyncio
import websockets

connected_clients = []

USAGE_LIMIT = 4 * 60 * 60 * 17 * 100

class UsageLimitException(Exception):
    pass


async def handler(websocket, path=None):
    global DATA_SENT
    print("Client connected")
    connected_clients.append(websocket)
    usage = 0
    try:
        while True:
            message = await websocket.recv()
            usage += len(message)
            
            if usage > USAGE_LIMIT:
                raise UsageLimitException(f"{usage:d} bytes sent. Connection closed.")

            # Forward the message to the other client
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except UsageLimitException as e:
        await websocket.close()
        print("Usage limit exceede. Connection closed.")
    finally:
        connected_clients.remove(websocket)


async def main():
    try:
        async with websockets.serve(handler, "0.0.0.0", 10000):
            print("Server started on ws://0.0.0.0:10000")
            await asyncio.Future()  # run forever
    except Exception as ex:
        print(ex.args[0])


if __name__ == "__main__":
    asyncio.run(main())
