from pydantic import BaseModel


class DeviceModel(BaseModel):
    device_name: str
    place: str
    state: bool
    device_type: str
    device_metadata: dict
