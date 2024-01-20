from core.database import get_db
from core.db_utils import get_obj_or_404
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..announcements.models import Announcement
from . import models, schemas

router = APIRouter()


@router.get(
    '/{id}/comments/',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ShowComment],
)
def get_all(id: int, db: Session = Depends(get_db)):
    """
    Get all comments from the database.
    """
    get_obj_or_404(Announcement, db, id=id)
    return db.query(models.Comment).filter(
        models.Comment.announcement_id == id
    )


@router.post(
    '/{id}/comments/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowComment,
)
def create(
    id: int, request: schemas.CreateComment,
    db: Session = Depends(get_db)
):
    """
    Creates a new comment based on
    the request data and adds it to the database.
    """
    get_obj_or_404(Announcement, db, id=id)
    request_data = request.dict()
    request_data['announcement_id'] = id
    comment = models.Comment(**request_data)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.patch(
    '/{id}/comments/{comment_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowComment,
)
def update(
    id: int,
    comment_id: int,
    request: schemas.UpdateComment,
    db: Session = Depends(get_db),
):
    """
    Updates a comment based on
    the request data and adds it to the database.
    """
    get_obj_or_404(Announcement, db, id=id)
    comment = get_obj_or_404(
        models.Comment, db, id=comment_id
    )
    comment.text = request.text
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete(
    '/{id}/comments/{comment_id}',
    status_code=status.HTTP_200_OK,
)
def delete(id: int, comment_id: int, db: Session = Depends(get_db)):
    """
    Deletes a comment based on
    the request data and adds it to the database.
    """
    get_obj_or_404(Announcement, db, id=id)
    comment = get_obj_or_404(
        models.Comment, db, id=comment_id, announcement_id=id
    )
    db.delete(comment)
    db.commit()
    return {'message': 'Комментарий удален'}
