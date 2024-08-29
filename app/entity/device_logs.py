from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.config.database_config import Base
from app.entity.device import Device


class DeviceLogs(Base):
    __tablename__ = 'device_logs'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(255), ForeignKey(Device.device_id, ondelete='CASCADE', onupdate='CASCADE'),
                       nullable=False)
    log = Column(Text, nullable=False)
    action = Column(String(255), nullable=True)
    timestamp = Column(DateTime, nullable=True, server_default=func.now())
