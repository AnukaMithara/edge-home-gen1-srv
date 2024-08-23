from fastapi import APIRouter, Response

from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.model.device_model import DeviceModel
from app.service.device_service import DeviceService

router = APIRouter(
    prefix="/v1/device",
    tags=["Device"]
)
logger = get_logger(class_name=__name__)
device_service = DeviceService()


@router.post("/add")
async def add_device(db: db_dependency, response: Response, device_model: DeviceModel):
    result = device_service.add_device(device_model=device_model, db=db)
    response.status_code = result.status_code
    return result


@router.get("/all")
async def get_all_devices(db: db_dependency, response: Response):
    result = device_service.get_all_devices(db=db)
    response.status_code = result.status_code
    return result
