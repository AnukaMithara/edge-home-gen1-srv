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


@router.put("/change_state/{device_id}/{state}")
async def change_device_state(db: db_dependency, response: Response, device_id: str, state: bool):
    result = await device_service.change_device_state(db=db, device_id=device_id, state=state)
    response.status_code = result.status_code
    return result


@router.post("/start_read_data/{device_id}")
def start_process(db: db_dependency, response: Response, device_id: str):
    result = device_service.start_read_data(db=db, device_id=device_id)
    response.status_code = result.status_code
    return result


@router.post("/stop_read_data/{device_id}")
def stop_process(db: db_dependency, response: Response, device_id: str):
    result = device_service.stop_read_data(db=db, device_id=device_id)
    response.status_code = result.status_code
    return result


@router.get("/video_feed/{device_id}")
def video_feed(device_id: str):
    return device_service.video_feed(device_id=device_id)


@router.post("/set_control_device")
async def set_control_device(db: db_dependency, response: Response, master_device_id: str, slave_device_id: str):
    result = device_service.set_control_device(db=db, master_device_id=master_device_id,
                                               slave_device_id=slave_device_id)
    response.status_code = result.status_code
    return result
