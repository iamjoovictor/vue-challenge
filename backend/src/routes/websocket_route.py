from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ..middleware.websocket_manager import manager
router = APIRouter(tags=["websocket"], prefix="/websocket")

@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)