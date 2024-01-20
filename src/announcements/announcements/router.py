from core.database import get_db
from core.db_utils import get_obj_or_404
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..categorys.models import Category
from . import models, schemas

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ShowAnnouncement],
)
def get_all(db: Session = Depends(get_db)):
    """
    Get all announcements from the database.
    """
    return db.query(models.Announcement).all()


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
def create(request: schemas.CreateAnnouncement, db: Session = Depends(get_db)):
    """
    Creates a new announcement based on
    the request data and adds it to the database.
    """
    get_obj_or_404(Category, db, id=request.category_id)
    announcement = models.Announcement(**request.dict())
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
    db: Session = Depends(get_db)
):
    """
    Updates an announcement by its ID.
    """
    announcement = get_obj_or_404(models.Announcement, db, id=id)
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
def delete(id: int, db: Session = Depends(get_db)):
    """
    Deletes an announcement by its ID.
    """
    announcement = get_obj_or_404(models.Announcement, db, id=id)
    db.delete(announcement)
    db.commit()
    return {'message': 'Объявление удалено'}
