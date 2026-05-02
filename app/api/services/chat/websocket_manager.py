from typing import Dict, List
from fastapi import WebSocket
import json
from datetime import datetime


class ConnectionManager:
    def __init__(self):
        # Dictionary to store active connections: chat_group_id -> list of websockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_group_id: str):
        """Connect a websocket to a chat group"""
        await websocket.accept()
        if chat_group_id not in self.active_connections:
            self.active_connections[chat_group_id] = []
        self.active_connections[chat_group_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_group_id: str):
        """Disconnect a websocket from a chat group"""
        if chat_group_id in self.active_connections:
            self.active_connections[chat_group_id].remove(websocket)
            if not self.active_connections[chat_group_id]:
                del self.active_connections[chat_group_id]

    async def broadcast_to_group(self, chat_group_id: str, message: dict):
        """Broadcast a message to all connected clients in a chat group"""
        if chat_group_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[chat_group_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    # Connection is dead, mark for removal
                    disconnected.append(connection)

            # Remove dead connections
            for dead_connection in disconnected:
                self.disconnect(dead_connection, chat_group_id)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific websocket"""
        try:
            await websocket.send_json(message)
        except Exception:
            pass


# Global connection manager instance
manager = ConnectionManager()