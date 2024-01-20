from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from core.database import Base


association_categorys_announcements = Table(
    'categorys_announcements',
    Base.metadata,
    Column(
        'category_id', ForeignKey('categorys.id'),
        primary_key=True, nullable=True,
    ),
    Column(
        'announcement_id', ForeignKey('announcements.id'),
        primary_key=True, nullable=True
    )
)


class Announcement(Base):
    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categorys.id'))

    author = relationship('User', back_populates='announcement')
    category = relationship(
        'Category', secondary=association_categorys_announcements,
        back_populates='announcements'
    )
    comments = relationship('Comment', back_populates='blog')
