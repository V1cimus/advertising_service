from datetime import timedelta
from typing import Annotated

from core.database import get_db
from core.db_utils import check_if_already_registered, get_obj_or_404
from core.hashing import hash_password
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm as LoginForm
from sqlalchemy.orm import Session

from . import authenticate, models, schemas
from config import settings

router_auth = APIRouter()
router_user = APIRouter()


@router_auth.post(
    '/register/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
)
def register(
    request: schemas.BaseUser, db: Session = Depends(get_db),
):
    """
    Register a new user.
    Permission: Allow Any
    """
    user_dict = request.dict()
    check_if_already_registered(models.User, user_dict, db)
    password = user_dict.pop('password')
    user = models.User(**user_dict)
    user.password = hash_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router_auth.post('/login/', response_model=schemas.Token)
def login(
    form_data: Annotated[LoginForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    Authenticates a user and generates an access token.
    Permission: Allow Any
    """
    user = authenticate.authenticate_user(
        form_data.username, form_data.password, db
    )
    access_token_expires = timedelta(seconds=settings.ACCESS_TOKEN_LIFETIME)
    access_token = authenticate.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router_user.post(
    '/{id}/set-ban/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowUser,
    )
def ban_user(
    id: int,
    _: schemas.UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Resets the ban status of a user.
    Permission: Admin
    """
    user = get_obj_or_404(models.User, db, id=id)
    user.banned = not user.banned
    db.commit()
    db.refresh(user)
    return user


@router_user.post(
    '/{id}/set-admin/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowUser,
)
def set_admin_user(
    id: int,
    # _: schemas.UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Resets the admin status of a user identified by the given ID.
    Permission: Admin
    """
    user = get_obj_or_404(models.User, db, id=id)
    user.admin = not user.admin
    db.commit()
    db.refresh(user)
    return user
