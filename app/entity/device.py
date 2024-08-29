from sqlalchemy import Column, BigInteger, String, Boolean, Date, JSON

from app.config.database_config import Base


class Device(Base):
    __tablename__ = 'device'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String(255), unique=True, nullable=False)
    device_name = Column(String(255), nullable=False)
    place = Column(String(255), nullable=False)
    state = Column(Boolean, default=False)
    device_type = Column(String(100), nullable=True)
    device_metadata = Column(JSON, nullable=True)
