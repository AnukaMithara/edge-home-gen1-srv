from pydantic import BaseModel
from typing import Optional


class DeviceMetadata(BaseModel):
    connection_type: Optional[str]
    mac_address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    url: Optional[str] = None


class DeviceModel(BaseModel):
    device_name: str
    place: str
    device_type: str
    device_metadata: Optional[DeviceMetadata] = None
