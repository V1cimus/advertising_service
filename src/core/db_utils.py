from getpass import getpass
from typing import Any, Type

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session
from users import models, schemas

from .database import SessionLocal
from .hashing import hash_password

db = SessionLocal()


def check_if_already_registered(
            model: BaseModel, fields: dict, db: Session
        ) -> None:
    """
    Check if the given model and fields are already registered in the database.
    """
    fields = [
        getattr(model, key) == value for key, value in fields.items()
    ]
    if db.query(model).filter(or_(*fields)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{model.__name__} уже существует',
        )


def get_obj_or_404(model: Type[BaseModel], db: Session, **kwargs: Any):
    """
    Retrieve an object from the database based on its ID or
    raise a 404 error if not found.
    """
    try:
        obj = db.query(model).filter_by(**kwargs).first()
    except Exception as e:
        raise e

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{model.__name__} с такими данными не существует',
        )
    return obj


def create_superuser() -> str:
    """
    Create a super user with the given username, email, and password.
    """
    username = input('Введите имя пользователя: ')
    if db.query(models.User).filter(models.User.username == username).first():
        return f'Пользователь {username} уже существует'

    email = input('Введите адрес электронной почты: ')
    if db.query(models.User).filter(models.User.email == email).first():
        return f'Пользователь c {email} уже существует'

    password = getpass('Введите пароль: ')

    try:
        schemas.BaseUser(username=username, email=email, password=password)
    except ValueError as e:
        return e

    password = hash_password(password)
    user = models.User(username=username, email=email, password=password)
    user.admin = True
    user.superuser = True
    db.add(user)
    db.commit()
    db.refresh(user)

    return 'Superuser успешно создан!'
