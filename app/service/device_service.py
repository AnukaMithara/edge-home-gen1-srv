import asyncio

from app.entity.control_device_permission import CotrolDevicePermission
from app.entity.device import Device
from app.entity.device_logs import DeviceLogs

from app.model.generic_response import GenericResponse
from app.config.logging_config import get_logger
from app.repository.control_device_permission_repository import CotrolDevicePermissionRepository
from app.repository.device_logs_repository import DeviceLogsRepository
from app.repository.device_repository import DeviceRepository
from app.service.face_recognition_service import FaceRecognitionService
from app.service.websocket_service import WebsocketService

logger = get_logger(class_name=__name__)
websocket_service = WebsocketService()


class DeviceService:

    @classmethod
    def add_device(cls, device_model, db):
        try:
            logger.info("Add Device Process Started")

            last_id = DeviceRepository.get_last_id(db=db)
            device_id = f'{device_model.device_type}_{last_id + 1}'

            device = Device(
                device_name=device_model.device_name,
                device_id=device_id,
                place=device_model.place,
                state=False,
                device_type=device_model.device_type,
                device_metadata=device_model.device_metadata.dict()
            )

            device = DeviceRepository.save(device=device, db=db)

            device_logs = DeviceLogs(
                device_id=device.device_id,
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

    @classmethod
    async def change_device_state(cls, db, device_id, state):
        try:
            logger.info("Change Device State Process Started")

            device = DeviceRepository.get_by_device_id(device_id=device_id, db=db)
            if not device:
                logger.info("Change Device State Process End with error")
                return GenericResponse.failed(message="Device not found", results=[], status_code=404)

            logger.info(f"Sending message to device {device_id}")
            device_message = {
                "message_type": "manual_state_change",
                "message": f"Device {device.device_name} {'activated' if state else 'deactivated'}",
                "is_authenticated": state
            }

            message_sent = False
            attempt = 10
            while not message_sent and attempt > 0:
                try:
                    device_websocket = websocket_service.get_active_connections_dict().get(device_id)
                    await websocket_service.send_personal_message(device_message, device_websocket)
                    message_sent = True
                    logger.info(f"Message sent to device {device_id}")
                except Exception as ex:
                    logger.error(f"Error sending message to device {device_id}: {str(ex)}")
                    await asyncio.sleep(2)
                    attempt -= 1

            # update device status
            DeviceRepository.update_device_state(device_id, state, db)

            device_logs = DeviceLogs(
                device_id=device.device_id,
                log=f"Device {device.device_name} {'activated' if state else 'deactivated'}",
                action="state_change"
            )

            DeviceLogsRepository.save(device_logs=device_logs, db=db)

            logger.info("Change Device State Process End")
            return GenericResponse.success(message="Device state changed", results=device)
        except Exception as ex:
            logger.error(f"Change Device State Error: {str(ex)}")
            logger.info("Change Device State End With Error")
            return GenericResponse.failed(message=f"Change Device State Failed, Error: {str(ex)}", results=[])

    @classmethod
    def start_read_data(cls, db, device_id):
        try:
            logger.info("Start read data Process Started")

            device = DeviceRepository.get_by_device_id(device_id=device_id, db=db)
            if not device:
                logger.info("Start read data Process End with error")
                return GenericResponse.failed(message="Device not found", results=[], status_code=404)

            # get controlled device from the read device
            controlled_devices = CotrolDevicePermissionRepository.get_all_controled_device(device_id=device_id, db=db)
            target_device_id = None
            if device.device_type == 'CAMERA':
                camera_url = device.device_metadata.get('url')
                for controlled_device in controlled_devices:
                    target_device = DeviceRepository.get_by_device_id(device_id=controlled_device.slave_device_id,
                                                                      db=db)
                    if target_device and target_device.device_type == 'DOOR_LOCK':
                        target_device_id = target_device.device_id

                if not camera_url:
                    logger.info("Start read data Process End with error")
                    return GenericResponse.failed(message="Camera not found", results=[], status_code=404)

                if not target_device_id:
                    logger.info("Start read data Process End with error")
                    return GenericResponse.failed(message="Target device not found", results=[], status_code=404)

                FaceRecognitionService.start_capture(device_id=device_id, target_device_id=target_device_id,
                                                     cam_source=camera_url)

                device_logs = DeviceLogs(
                    device_id=device.device_id,
                    log=f"Device {device.device_name} data reading started",
                    action="start_process"
                )

                DeviceLogsRepository.save(device_logs=device_logs, db=db)
            else:
                logger.info("Start read data Process End with error")
                return GenericResponse.failed(message="Device type not supported", results=[], status_code=404)

            logger.info("Start Process Process End")
            return GenericResponse.success(message="Device process started", results=device)
        except Exception as ex:
            logger.error(f"Start Process Error: {str(ex)}")
            logger.info("Start Process End With Error")
            return GenericResponse.failed(message=f"Start Process Failed, Error: {str(ex)}", results=[])

    @classmethod
    def stop_read_data(cls, db, device_id):
        try:
            logger.info("Stop read data Process Started")

            device = DeviceRepository.get_by_device_id(device_id=device_id, db=db)
            if not device:
                logger.info("Stop read data Process End with error")
                return GenericResponse.failed(message="Device not found", results=[], status_code=404)

            is_stopped = FaceRecognitionService.stop_process(device_id=device_id)
            if not is_stopped:
                logger.info("Not available any process to stop")
                return GenericResponse.success(message="Not available any process to stop", results=[])

            device_logs = DeviceLogs(
                device_id=device.device_id,
                log=f"Device {device.device_name} data reading stopped",
                action="stop_process"
            )

            DeviceLogsRepository.save(device_logs=device_logs, db=db)

            logger.info("Stop Process Process End")
            return GenericResponse.success(message="Device process stopped", results=device)
        except Exception as ex:
            logger.error(f"Stop Process Error: {str(ex)}")
            logger.info("Stop Process End With Error")
            return GenericResponse.failed(message=f"Stop Process Failed, Error: {str(ex)}", results=[])

    @classmethod
    def video_feed(cls, device_id):
        return FaceRecognitionService.video_feed(device_id=device_id)

    @classmethod
    def set_control_device(cls, db, master_device_id, slave_device_id):
        try:
            logger.info("Set Control Device Process Started")

            device = DeviceRepository.get_by_device_id(device_id=master_device_id, db=db)
            control_device = DeviceRepository.get_by_device_id(device_id=slave_device_id, db=db)
            if not device or not control_device:
                logger.info("Set Control Device Process End with error")
                return GenericResponse.failed(message="Device not found", results=[], status_code=404)

            control_permission = CotrolDevicePermissionRepository.get_by_device_ids(master_device_id=master_device_id,
                                                                                    slave_device_id=slave_device_id,
                                                                                    db=db)
            if control_permission:
                logger.info("Set Control Device Process End with error")
                return GenericResponse.failed(message="Control permission already exists", results=[], status_code=400)

            relation = CotrolDevicePermission(
                master_device_id=master_device_id,
                slave_device_id=slave_device_id
            )

            control_permission = CotrolDevicePermissionRepository.save(relation=relation, db=db)

            device_logs = DeviceLogs(
                device_id=device.device_id,
                log=f"Device {device.device_name} control permission set to {control_device.device_name}",
                action="set_control"
            )

            DeviceLogsRepository.save(device_logs=device_logs, db=db)

            logger.info("Set Control Device Process End")
            return GenericResponse.success(message="Control permission set", results=control_permission)
        except Exception as ex:
            logger.error(f"Set Control Device Error: {str(ex)}")
            logger.info("Set Control Device End With Error")
            return GenericResponse.failed(message=f"Set Control Device Failed, Error: {str(ex)}", results=[])
