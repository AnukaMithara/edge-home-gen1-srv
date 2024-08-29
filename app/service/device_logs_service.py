from app.model.generic_response import GenericResponse
from app.config.logging_config import get_logger
from app.repository.device_logs_repository import DeviceLogsRepository

logger = get_logger(class_name=__name__)


class DeviceLogsService:

    @classmethod
    def get_all_device_logs(cls, db):
        try:
            logger.info("Get All Device Logs Process Started")

            device_logs = DeviceLogsRepository.get_all(db=db)

            logger.info("Get All Device Logs Process End")
            return GenericResponse.success(message="Device Logs fetched", results=device_logs)
        except Exception as ex:
            logger.error(f"Get All Device Logs Error: {str(ex)}")
            logger.info("Get All Device Logs End With Error")
            return GenericResponse.failed(message=f"Get All Device Logs Failed, Error: {str(ex)}", results=[])

    @classmethod
    def get_device_logs_by_device_id(cls, device_id, db):
        try:
            logger.info("Get Device Logs By Device Id Process Started")

            device_logs = DeviceLogsRepository.get_device_logs_by_device_id(device_id=device_id, db=db)

            logger.info("Get Device Logs By Device Id Process End")
            return GenericResponse.success(message="Device Logs fetched", results=device_logs)
        except Exception as ex:
            logger.error(f"Get Device Logs By Device Id Error: {str(ex)}")
            logger.info("Get Device Logs By Device Id End With Error")
            return GenericResponse.failed(message=f"Get Device Logs By Device Id Failed, Error: {str(ex)}", results=[])
