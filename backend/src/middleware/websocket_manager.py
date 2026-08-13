import json

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    def _normalize_payload(self, item):
        if isinstance(item, str):
            try:
                return json.loads(item)
            except (TypeError, json.JSONDecodeError):
                return {"message": item}
        return item

    async def send(self, item: dict, websocket: WebSocket):
        await websocket.send_json(self._normalize_payload(item))

    async def broadcast(self, item: dict):
        payload = self._normalize_payload(item)
        for connection in self.active_connections:
            await connection.send_json(payload)


manager = ConnectionManager()
managerCommunications = ConnectionManager()