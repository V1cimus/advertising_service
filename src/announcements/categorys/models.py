from core.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..announcements.models import association_categorys_announcements


class Category(Base):
    __tablename__ = 'categorys'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    announcements = relationship(
        'Announcement', secondary=association_categorys_announcements,
        back_populates='category',
    )
