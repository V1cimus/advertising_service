from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import settings

dbsettings = settings.DATA_BASE

DATABASE_URL = (
    f'{dbsettings.DB_ENGINE}://'
    + f'{dbsettings.POSTGRES_USER}:{dbsettings.POSTGRES_PASSWORD}'
    + f'@{dbsettings.DB_HOST}:{dbsettings.DB_PORT}/{dbsettings.DB_NAME}'
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    """
    Returns a database session.

    Returns:
        A generator that yields a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
