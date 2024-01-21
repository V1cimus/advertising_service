from datetime import datetime

from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    announcement_id = Column(Integer, ForeignKey('announcements.id'))
    text = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    author = relationship('User', back_populates='comment')
    announcement = relationship('Announcement', back_populates='comments')
