from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, DateTime, func

from app.config.database_config import Base
from app.entity.user import User


class UserLogs(Base):
    __tablename__ = 'user_logs'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_email = Column(String(255), ForeignKey(User.email, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    log = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=True, server_default=func.now())
