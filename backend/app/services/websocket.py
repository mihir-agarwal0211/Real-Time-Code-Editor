from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    """Manages active WebSocket connections for real-time collaboration."""

    def __init__(self):
        self.active_sessions: Dict[str, List[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        """Adds a new WebSocket connection to the session."""
        await websocket.accept()
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = []
        self.active_sessions[session_id].append(websocket)

    async def send_code_update(self, session_id: str, message: str):
        """Broadcasts a code update to all users in the same session."""
        if session_id in self.active_sessions:
            for connection in self.active_sessions[session_id]:
                await connection.send_text(message)

    async def disconnect(self, session_id: str, websocket: WebSocket):
        """Removes a WebSocket connection from the session."""
        self.active_sessions[session_id].remove(websocket)
        if not self.active_sessions[session_id]:  
            del self.active_sessions[session_id]

manager = ConnectionManager()
