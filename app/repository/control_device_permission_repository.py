from app.exceptions.exception import DbOperationException
from app.entity.control_device_permission import CotrolDevicePermission


class CotrolDevicePermissionRepository:

    @classmethod
    def save(cls, relation, db):
        try:
            db.add(relation)
            db.commit()
            db.refresh(relation)
            return relation
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_all_controled_device(cls, device_id, db):
        try:
            return db.query(CotrolDevicePermission).filter(
                CotrolDevicePermission.master_device_id == device_id
            ).all()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)

    @classmethod
    def get_by_device_ids(cls, master_device_id, slave_device_id, db):
        try:
            return db.query(CotrolDevicePermission).filter(
                CotrolDevicePermission.master_device_id == master_device_id,
                CotrolDevicePermission.slave_device_id == slave_device_id
            ).first()
        except Exception as ex:
            raise DbOperationException(str(ex), ex)
