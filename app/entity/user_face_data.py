from sqlalchemy import Column, BigInteger, ForeignKey, BLOB, DateTime, func
from sqlalchemy.orm import relationship

from app.config.database_config import Base
from app.entity.user import User


class UserFaceData(Base):
    __tablename__ = 'user_face_data'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(User.id, ondelete='CASCADE', onupdate='CASCADE'))
    face_data = Column(BLOB, nullable=False)
    created_at = Column(DateTime, nullable=True, server_default=func.now())

    user = relationship("User", back_populates="user_face_data", lazy="joined", innerjoin=True)
