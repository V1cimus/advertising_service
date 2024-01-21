from core.database import get_db
from core.db_utils import get_obj_or_404
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..categorys.models import Category
from . import models, schemas
from .filters import AnnouncementFilter
from users import authenticate
from users.schemas import UserInDB

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=Page[schemas.ShowAnnouncement],
)
def get_all(
    items_filter: AnnouncementFilter = FilterDepends(AnnouncementFilter),
    db: Session = Depends(get_db),
) -> Page[schemas.ShowAnnouncement]:
    """
    Get all announcements from the database.
    """
    announcements = select(models.Announcement)
    announcements = items_filter.filter(announcements)
    announcements = items_filter.sort(announcements)
    return paginate(db, announcements)


@router.get(
    '/{id}/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowAnnouncement,
)
def get_by_id(id: int, db: Session = Depends(get_db)):
    """
    Get an announcement by its ID.
    """
    return get_obj_or_404(models.Announcement, db, id=id)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowAnnouncement,
)
def create(
    request: schemas.CreateAnnouncement,
    user: UserInDB = Depends(authenticate.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Creates a new announcement based on
    the request data and adds it to the database.
    """
    request_data = request.dict()
    request_data['author_id'] = user.id
    get_obj_or_404(Category, db, id=request.category_id)
    announcement = models.Announcement(**request_data)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


@router.patch(
    '/{id}/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowAnnouncement,
)
def update(
    id: int, request: schemas.UpdateAnnouncement,
    user: UserInDB = Depends(authenticate.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Updates an announcement by its ID.
    """
    announcement = get_obj_or_404(models.Announcement, db, id=id)
    if announcement.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Нельзя редактировать чужое объявление'
        )
    if request.category_id is not None:
        get_obj_or_404(Category, db, id=request.category_id)
    for key, value in request.dict().items():
        if value is not None:
            print(key, value)
            setattr(announcement, key, value)
    print(announcement.__dict__)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


@router.delete(
    '/{id}/',
    status_code=status.HTTP_200_OK,
)
def delete(
    id: int,
    user: UserInDB = Depends(authenticate.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Deletes an announcement by its ID.
    """
    announcement = get_obj_or_404(models.Announcement, db, id=id)
    if announcement.author_id == user.id or user.admin:
        db.delete(announcement)
        db.commit()
        return {'message': 'Объявление удалено'}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Вы не можете удалить это объявление'
    )
