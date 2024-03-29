from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    superuser = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    announcement = relationship('Announcement', back_populates='author')
    comment = relationship('Comment', back_populates='author')
    review = relationship('Review', back_populates='author')
