from core.database import get_db
from core.db_utils import get_obj_or_404
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..announcements.models import Announcement
from . import models, schemas
from users import authenticate
from users.schemas import UserInDB

router = APIRouter()


@router.get(
    '/{id}/complaints/',
    status_code=status.HTTP_200_OK,
    response_model=Page[schemas.ShowComplaint],
)
def get_all(
    id: int,
    _: UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Get all complaints from the database.
    Permission: Admin
    """
    get_obj_or_404(Announcement, db, id=id)
    return paginate(db, select(models.Complaint).where(
        models.Complaint.announcement_id == id
    ))


@router.get(
    '/{id}/complaints/{complaint_id}/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowComplaint,
)
def get_by_id(
    id: int,
    complaint_id: int,
    _: UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Get a complaint by its ID.
    Permission: Admin
    """
    get_obj_or_404(Announcement, db, id=id)
    return get_obj_or_404(
        models.Complaint, db, id=complaint_id
    )


@router.post(
    '/{id}/complaints/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowComplaint,
)
def create(
    id: int,
    request: schemas.CreateComplaint,
    db: Session = Depends(get_db),
):
    """
    Creates a new complaint based on
    the request data and adds it to the database.
    Permission: Allow Any
    """
    get_obj_or_404(Announcement, db, id=id)
    complaint = models.Complaint(**request.dict())
    complaint.announcement_id = id
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.delete(
    '/complaints/{complaint_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    complaint_id: int,
    _: UserInDB = Depends(authenticate.get_current_admin_user),
    db: Session = Depends(get_db),
):
    """
    Delete a complaint by its ID.
    Permission: Admin
    """
    complaint = get_obj_or_404(
        models.Complaint, db, id=complaint_id
    )
    db.delete(complaint)
    db.commit()
