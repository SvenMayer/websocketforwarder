# -*- coding: utf-8 -*-
import asyncio
import websockets
import websockets.asyncio
import websockets.asyncio.server
import websockets.http11

connected_clients = []

USAGE_LIMIT = 4 * 60 * 60 * 17 * 100

class UsageLimitException(Exception):
    pass


async def handler_request(connection, request):
    print("handler")
    if request.path == "/health":
        return connection.respond(HTTPStatus.OK, "OK\n")

    if request.headers.get("Upgrade") is None:
        return connection.respond(
            HTTPStatus.BAD_REQUEST, "Missing websocket Upgrade header\n"
        )

#    if request.headers.get("User-Agent", "").startswith("RadioPad/"):
#        setattr(connection, "is_radio_pad", True)

    return None


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
    async with websockets.serve(handler, "0.0.0.0", 10000, process_request=handler_request):
        print("Server started on ws://0.0.0.0:10000")
        await asyncio.Future()  # run ,


if __name__ == "__main__":
    asyncio.run(main())
