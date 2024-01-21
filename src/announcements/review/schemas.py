from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from users.schemas import ShowUser


class ShowReview(BaseModel):
    id: int
    author: ShowUser
    text: str
    created_at: datetime
    announcement_id: int


class CreateReview(BaseModel):
    text: str = Field(max_length=4096)

    class Config:
        from_attributes = True


class UpdateReview(BaseModel):
    text: Optional[str] = Field(None, max_length=4096)

    class Config:
        from_attributes = True
