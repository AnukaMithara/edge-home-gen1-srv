from sqlalchemy import Column, BigInteger, ForeignKey, String
from app.entity.device import Device
from app.config.database_config import Base


class CotrolDevicePermission(Base):
    __tablename__ = 'control_device_permission'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    master_device_id = Column(String(255), ForeignKey(Device.device_id, ondelete='CASCADE', onupdate='CASCADE'),
                              nullable=False)
    slave_device_id = Column(String(255), ForeignKey(Device.device_id, ondelete='CASCADE', onupdate='CASCADE'),
                             nullable=False)
