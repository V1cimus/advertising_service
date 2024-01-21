from datetime import datetime

from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Complaint(Base):
    __tablename__ = 'complaint'

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey('announcements.id'))
    text = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    announcement = relationship('Announcement', back_populates='complaint')
