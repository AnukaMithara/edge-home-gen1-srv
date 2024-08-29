from pydantic import BaseModel


class NotificationModel(BaseModel):
    client_id: str
    message: dict
