from datetime import datetime, timedelta
from typing import Annotated

from core.database import SessionLocal
from core.db_utils import get_obj_or_404
from core.hashing import verify_password
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .models import User as DB_User
from .schemas import UserInDB
from config import settings

db = SessionLocal()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates an access token using the provided data and optional
    expiration delta.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def get_user(db: Session, email: str):
    """
    Retrieves a user from the database based on the given email.
    """
    user = get_obj_or_404(DB_User, db, email=email)
    user_dict = {key: value for key, value in user.__dict__.items()
                 if key != '_sa_instance_state'}
    return UserInDB(**user_dict)


def authenticate_user(email: str, password: str, db: Session):
    """
    Authenticates a user by checking if the given username
    and password match an entry in the database.
    """
    user = get_user(db=db, email=email)
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль',
        )
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Get the current user based on the provided token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    current_user = get_user(db=db, username=username)
    if current_user is None:
        raise credentials_exception
    return current_user
