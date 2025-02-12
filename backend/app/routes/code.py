from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket import manager

router = APIRouter()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(session_id: str, websocket: WebSocket):
    """Handles real-time code editing via WebSockets."""
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Receive changes from user
            await manager.send_code_update(session_id, data)  # Broadcast updates
    except WebSocketDisconnect:
        await manager.disconnect(session_id, websocket)
