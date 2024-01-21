from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from . import models, schemas
from core.database import get_db
from core.db_utils import check_if_already_registered, get_obj_or_404
from users import authenticate
from users.schemas import UserInDB

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Category],
)
def get_all(db: Session = Depends(get_db)):
    """
    Get all categories from the database.
    Permission: Allow Any
    """
    return db.query(models.Category).all()


@router.get(
    '/{id}/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Category,
)
def get_by_id(id: int, db: Session = Depends(get_db)):
    """
    Get a category by its ID.
    Permission: Allow Any
    """
    return get_obj_or_404(models.Category, db, id=id)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShortCategory,
)
def create(
    request: schemas.ShortCategory,
    _: UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Creates a new category based on
    the request data and adds it to the database.
    Permission: Admin
    """
    check_if_already_registered(models.Category, request.dict(), db)
    category = models.Category(**request.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.patch(
    '/{id}/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShortCategory,
)
def update(
    id: int, request: schemas.ShortCategory,
    _: UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Update a category by ID.
    Permission: Admin
    """
    category = get_obj_or_404(models.Category, db, id=id)
    category.name = request.name
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete(
    '/{id}/',
    status_code=status.HTTP_200_OK,
)
def delete(
    id: int,
    _: UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Deletes a category by its ID.
    Permission: Admin
    """
    category = get_obj_or_404(models.Category, db, id=id)
    db.delete(category)
    db.commit()
    return {'message': 'Категория удалена'}
