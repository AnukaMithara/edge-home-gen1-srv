from app.entity.device import Device
from app.entity.device_logs import DeviceLogs

from app.model.generic_response import GenericResponse
from app.config.logging_config import get_logger
from app.repository.device_logs_repository import DeviceLogsRepository
from app.repository.device_repository import DeviceRepository

logger = get_logger(class_name=__name__)


class DeviceService:

    @classmethod
    def add_device(cls, device_model, db):
        try:
            logger.info("Add Device Process Started")

            device = Device(
                device_name=device_model.device_name,
                place=device_model.place,
                state=device_model.state,
                device_type=device_model.device_type,
                device_metadata=device_model.device_metadata
            )

            device = DeviceRepository.save(device=device, db=db)

            device_logs = DeviceLogs(
                device_id=device.id,
                log=f"Device {device.device_name} added",
                action="add"
            )

            DeviceLogsRepository.save(device_logs=device_logs, db=db)

            logger.info("Add Device Process End")
            return GenericResponse.success(message="Device added", results=device)
        except Exception as ex:
            logger.error(f"Add Device Error: {str(ex)}")
            logger.info("Add Device End With Error")
            return GenericResponse.failed(message=f"Add Device Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_all_devices(cls, db):
        try:
            logger.info("Get All Devices Process Started")

            devices = DeviceRepository.get_all(db=db)
            categorized_devices = cls.categorize_devices_for_place(devices)

            logger.info("Get All Devices Process End")
            return GenericResponse.success(message="Devices fetched", results=categorized_devices)
        except Exception as ex:
            logger.error(f"Get All Devices Error: {str(ex)}")
            logger.info("Get All Devices End With Error")
            return GenericResponse.failed(message=f"Get All Devices Failed, Error: {str(ex)}", results=[])

    @classmethod
    def categorize_devices_for_place(cls, devices):
        categorized_devices = {}
        for device in devices:
            if device.place not in categorized_devices:
                categorized_devices[device.place] = []
            categorized_devices[device.place].append(device)
        return categorized_devices
