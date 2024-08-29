from sqlalchemy import Column, BigInteger, ForeignKey, Enum, String

from app.config.database_config import Base
from app.entity.user import User
from app.entity.device import Device


class Permissions(Base):
    __tablename__ = 'permissions'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(User.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    device_id = Column(String(255), ForeignKey(Device.device_id, ondelete='CASCADE', onupdate='CASCADE'),
                       nullable=False)
    access_level = Column(Enum('read', 'write', 'admin', name="access_level"), default='read')
