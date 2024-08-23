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
