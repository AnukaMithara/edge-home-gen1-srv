from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, Boolean

from app.config.database_config import Base


class Source(Base):
    __tablename__ = 'source'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    source_name = Column(String(100))
    display_name = Column(String(100))
    source_category = Column(BigInteger, ForeignKey('source_category.id', ondelete='CASCADE', onupdate='CASCADE'))
    source_type = Column(BigInteger, ForeignKey('source_type.id', ondelete='CASCADE', onupdate='CASCADE'))
    credibility = Column(BigInteger, ForeignKey('credibility.id', ondelete='CASCADE', onupdate='CASCADE'))
    source_url = Column(Text)
    search_url = Column(Text)
    is_active = Column(Boolean, nullable=False, default=True)
