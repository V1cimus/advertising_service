from core.database import get_db
from core.db_utils import get_obj_or_404
from fastapi import APIRouter, Depends, HTTPException, status
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
    '/{id}/reviews/',
    status_code=status.HTTP_200_OK,
    response_model=Page[schemas.ShowReview],
)
def get_all(id: int, db: Session = Depends(get_db)):
    """
    Get all reviews from the database.
    Permission: Allow Any
    """
    get_obj_or_404(Announcement, db, id=id)
    return paginate(db, select(models.Review).where(
        models.Review.announcement_id == id
    ))


@router.get(
    '/{id}/reviews/{review_id}/',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowReview,
)
def get_by_id(
    id: int,
    review_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a review by its ID.
    Permission: Allow Any
    """
    get_obj_or_404(Announcement, db, id=id)
    return get_obj_or_404(models.Review, db, id=review_id)


@router.post(
    '/{id}/reviews/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowReview,
)
def create(
    id: int,
    request: schemas.CreateReview,
    user: UserInDB = Depends(authenticate.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Creates a new review based on
    the request data and adds it to the database.
    Permission: User
    """
    get_obj_or_404(Announcement, db, id=id)
    request_data = request.dict()
    request_data['author_id'] = user.id
    request_data['announcement_id'] = id
    review = models.Review(**request_data)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.patch(
    '/{id}/reviews/{review_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowReview,
)
def update(
    id: int,
    review_id: int,
    request: schemas.UpdateReview,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(authenticate.get_current_user),
):
    """
    Updates a review in the database.
    Permission: Author
    """
    get_obj_or_404(Announcement, db, id=id)
    review = get_obj_or_404(models.Review, db, id=review_id)
    if review.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Нельзя редактировать чужие отзывы'
        )
    for key, value in request.dict().items():
        if value is not None:
            setattr(review, key, value)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.delete(
    '/{id}/reviews/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete(
    id: int,
    review_id: int,
    db: Session = Depends(get_db),
    user: UserInDB = Depends(authenticate.get_current_user),
):
    """
    Deletes a review from the database.
    Permission: Author or Admin
    """
    get_obj_or_404(Announcement, db, id=id)
    review = get_obj_or_404(models.Review, db, id=review_id)
    if review.author_id == user.id or user.is_admin:
        db.delete(review)
        db.commit()
        return {'message': 'Отзыв удален'}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Нельзя редактировать чужие отзывы'
    )
