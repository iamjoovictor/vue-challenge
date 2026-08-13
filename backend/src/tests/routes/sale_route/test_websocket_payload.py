import json

import pytest

from src.middleware.websocket_manager import ConnectionManager


class FakeWebSocket:
    def __init__(self):
        self.sent = None

    async def send_json(self, item):
        self.sent = item


@pytest.mark.asyncio
async def test_broadcast_preserves_object_shape_for_websocket_clients():
    manager = ConnectionManager()
    expected = {"event": "sale_created", "product": "Laptop", "quantity": 2}
    websocket = FakeWebSocket()

    manager.active_connections = [websocket]

    await manager.broadcast(json.dumps(expected))

    assert websocket.sent == expected
