from fastapi import WebSocket, WebSocketDisconnect, HTTPException, APIRouter
from typing import Dict

from app.config.logging_config import get_logger
from app.model.notification_model import NotificationModel
from app.service.websocket_service import WebsocketService

router = APIRouter(
    prefix="/v1/notification",
    tags=["Notification"],
)
logger = get_logger(class_name=__name__)
websocket_service = WebsocketService()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    try:
        await websocket_service.connect(client_id, websocket)
        logger.info(f"Client #{client_id} connected")
        while True:
            data = await websocket.receive_json()
            await websocket_service.send_personal_message({"message": f"You said: {data}"}, websocket)
            await websocket_service.broadcast({"client_id": client_id, "message": data})
    except WebSocketDisconnect:
        websocket_service.disconnect(client_id)
        await websocket_service.broadcast({"message": f"Client #{client_id} left the chat"})


@router.post("/send-message/")
async def send_message(data: NotificationModel):
    active_connections = websocket_service.get_active_connections()
    if not active_connections:
        raise HTTPException(status_code=400, detail="No active WebSocket connections")

    websocket = websocket_service.get_active_connections_dict().get(data.client_id)
    if websocket:
        await websocket_service.send_personal_message(data.message, websocket)
        return {"status": "Message sent"}

    raise HTTPException(status_code=404, detail=f"Client #{data.client_id} not found")


@router.post("/broadcast/")
async def broadcast_message(message: Dict):
    active_connections = websocket_service.get_active_connections()
    if not active_connections:
        raise HTTPException(status_code=400, detail="No active WebSocket connections")

    await websocket_service.broadcast(message)
    return {"status": "Broadcast message sent"}


@router.get("/active-clients/")
async def get_active_clients():
    return {"active_connections": websocket_service.get_active_connections()}
