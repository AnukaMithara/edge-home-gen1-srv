from fastapi import APIRouter, Response

from app.config.database_config import db_dependency
from app.config.logging_config import get_logger
from app.service.device_logs_service import DeviceLogsService

router = APIRouter(
    prefix="/v1/device_logs",
    tags=["Device Logs"]
)
logger = get_logger(class_name=__name__)
device_log_service = DeviceLogsService()


@router.get("/all")
async def get_all_device_logs(db: db_dependency, response: Response):
    result = device_log_service.get_all_device_logs(db=db)
    response.status_code = result.status_code
    return result


@router.get("/get/{device_id}")
async def get_device_logs_by_device_id(db: db_dependency, response: Response, device_id: int):
    result = device_log_service.get_device_logs_by_device_id(device_id=device_id, db=db)
    response.status_code = result.status_code
    return result
