import asyncio
import websockets
import json

PORT = 9090
clients = {}  # {websocket: {"name": str, "color": [r,g,b], "pos": [x,y], "typing": bool}}
chat_log = []

async def notify_all():
    """Отправить всем текущее состояние"""
    if clients:
        state = {
            "players": {id(ws): data for ws, data in clients.items()},
            "chat": chat_log,
        }
        message = json.dumps(state)
        await asyncio.wait([ws.send(message) for ws in clients])

async def handler(websocket):
    try:
        # первый пакет = регистрация
        data = await websocket.recv()
        data = json.loads(data)
        clients[websocket] = {
            "name": data["name"],
            "color": data["color"],
            "pos": [400, 300],
            "typing": False
        }
        await notify_all()

        async for message in websocket:
            packet = json.loads(message)

            if packet["type"] == "pos":
                clients[websocket]["pos"] = packet["pos"]

            elif packet["type"] == "chat":
                chat_log.append((clients[websocket]["name"], packet["msg"]))
                chat_log[:] = chat_log[-10:]

            elif packet["type"] == "typing":
                clients[websocket]["typing"] = packet["status"]

            await notify_all()
    except:
        pass
    finally:
        if websocket in clients:
            del clients[websocket]
            await notify_all()

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"[SERVER] WebSocket сервер запущен на порту {PORT}")
        await asyncio.Future()  # бесконечный await

asyncio.run(main())