from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..categorys.schemas import Category
from ..comments.schemas import ShowShortComment
from users.schemas import ShowUser


class ShowAnnouncement(BaseModel):
    id: int
    author: ShowUser
    title: str
    content: str
    category: Category
    created_at: Optional[datetime] = datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )
    comments: List[ShowShortComment]


class ShowShortAnnouncement(BaseModel):
    id: int
    title: str
    category: Category
    author: ShowUser


class CreateAnnouncement(BaseModel):
    category_id: int
    title: str = Field(max_length=128)
    content: str = Field(max_length=4096)

    class Config:
        from_attributes = True


class UpdateAnnouncement(BaseModel):
    category_id: Optional[int] = Field(None)
    title: Optional[str] = Field(None, max_length=128)
    content: Optional[str] = Field(None, max_length=4096)

    class Config:
        from_attributes = True
