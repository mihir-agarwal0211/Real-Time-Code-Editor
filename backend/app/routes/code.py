from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket import manager
import json

router = APIRouter()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(session_id: str, websocket: WebSocket):
    """Handles real-time code editing and cursor updates via WebSockets."""
    await manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            # Broadcast both code changes & cursor updates
            if parsed_data["type"] == "code":
                await manager.send_code_update(session_id, json.dumps(parsed_data))
            
            elif parsed_data["type"] == "cursor":
                print(f"🖱 Received Cursor Update from {data}")
                # ✅ Extract user ID from message and broadcast it
                await manager.send_cursor_update(session_id, json.dumps({
                    "type": "cursor",
                    "user": parsed_data["user"],  # ✅ Includes userId
                    "cursor": parsed_data["cursor"]
                }))

    except WebSocketDisconnect:
        await manager.disconnect(session_id, websocket)
        print(f"🔴 User disconnected from session {session_id}")





