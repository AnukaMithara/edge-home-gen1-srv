from app.exceptions.exception import DbOperationException
from app.entity.device import Device


class DeviceRepository:

    @classmethod
    def save(cls, device, db):
        try:
            db.add(device)
            db.commit()
            db.refresh(device)
            return device
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_all(cls, db):
        try:
            return db.query(Device).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_by_device_id(cls, device_id, db):
        try:
            return db.query(Device).filter(Device.device_id == device_id).first()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_last_id(cls, db):
        try:
            device = db.query(Device).order_by(Device.id.desc()).first()
            return device.id if device else 0
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def update_device_state(cls, device_id, state, db):
        try:
            device = db.query(Device).filter(Device.device_id == device_id).first()
            device.state = state
            db.commit()
            return device
        except Exception as ex:
            raise DbOperationException(str(ex), ex)