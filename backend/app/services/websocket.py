from fastapi import WebSocket
from typing import Dict, List
from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import EditingSession
import json
from datetime import datetime

class ConnectionManager:
    """Manages active WebSocket connections for real-time collaboration."""

    def __init__(self):
        self.active_sessions: Dict[str, List[WebSocket]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        """Adds a new WebSocket connection to the session."""
        await websocket.accept()
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = {}
            self.cursors[session_id] = {}

        self.active_sessions[session_id] = websocket
        self.cursors[session_id] = {"lineNumber": 1, "column": 1}  # Default cursor position


        # # ✅ Store user as active in DB
        # db = SessionLocal()
        # session = db.query(EditingSession).filter_by(file_id=session_id, user_id=user_id).first()
        # if session:
        #     session.is_active = True
        #     db.commit()
        # else:
        #     new_session = EditingSession(file_id=session_id, user_id=user_id, cursor_position='{"lineNumber": 1, "column": 1}', is_active=True)
        #     db.add(new_session)
        #     db.commit()
        # db.close()

    async def send_code_update(self, session_id: str, message: str):
        """Broadcasts a code update to all users in the same session."""
        if session_id in self.active_sessions:
            for connection in self.active_sessions[session_id]:
                await connection.send_text(message)

    async def send_cursor_update(self, session_id: str, cursor: dict):
        """Updates cursor position in memory & notifies all users."""
        self.cursors[session_id] = cursor  # Store cursor in memory

        # Notify all users
        message = json.dumps({"type": "allCursors", "cursors": self.cursors[session_id]})
        for ws in self.active_sessions.get(session_id, {}).values():
            await ws.send_text(message)

    async def disconnect(self, session_id: str, websocket: WebSocket):
        """Removes a WebSocket connection from the session."""
        self.active_sessions[session_id].remove(websocket)
        if not self.active_sessions[session_id]:  
            del self.active_sessions[session_id]

manager = ConnectionManager()
