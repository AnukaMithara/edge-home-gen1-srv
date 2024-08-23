from app.entity.device_logs import DeviceLogs
from app.exceptions.exception import DbOperationException


class DeviceLogsRepository:

    @classmethod
    def save(cls, device_logs, db):
        try:
            db.add(device_logs)
            db.commit()
            db.refresh(device_logs)
            return device_logs
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_all(cls, db):
        try:
            return db.query(DeviceLogs).order_by(DeviceLogs.timestamp.desc()).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_device_logs_by_device_id(cls, device_id, db):
        try:
            return db.query(DeviceLogs).filter(DeviceLogs.device_id == device_id).order_by(
                DeviceLogs.timestamp.desc()).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)
