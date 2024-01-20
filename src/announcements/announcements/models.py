from core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..comments.models import Comment


class Announcement(Base):
    __tablename__ = 'announcements'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categorys.id'))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    author = relationship('User', back_populates='announcement')
    category = relationship('Category', back_populates='announcements')
    comments = relationship(Comment, back_populates='announcement')
