from sqlalchemy import Boolean, Column, Integer, String

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
