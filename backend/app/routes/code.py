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
            await manager.send_code_update(session_id, json.dumps(parsed_data))
            print(f"📩 Received WebSocket Message: {parsed_data}")  # Debugging

            if parsed_data["type"] == "cursor":
                print(f"📍 Cursor update received from {parsed_data['user']}: {parsed_data['cursor']}")
                await manager.send_cursor_update(session_id, json.dumps(parsed_data))

    except WebSocketDisconnect:
        await manager.disconnect(session_id, websocket)
        print(f"🔴 User disconnected from session {session_id}")





