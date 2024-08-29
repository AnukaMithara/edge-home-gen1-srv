from fastapi import WebSocket
from typing import Dict
from app.config.logging_config import get_logger

logger = get_logger(class_name=__name__)
active_connections: Dict[str, WebSocket] = {}


class WebsocketService:

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        active_connections.pop(client_id, None)

    async def send_personal_message(self, message: Dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: Dict):
        for connection in active_connections.values():
            await connection.send_json(message)

    def get_active_connections(self) -> int:
        return len(active_connections)

    def get_active_connections_dict(self) -> Dict[str, WebSocket]:
        return active_connections
