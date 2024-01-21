from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    announcement_id = Column(Integer, ForeignKey('announcements.id'))
    text = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    author = relationship('User', back_populates='review')
    announcement = relationship('Announcement', back_populates='reviews')
