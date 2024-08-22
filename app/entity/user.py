from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from app.config.database_config import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    role = Column(String(50), default='user')
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    user_face_data = relationship("UserFaceData", back_populates="user", lazy='noload')