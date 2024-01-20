from typing import Optional

from pydantic import BaseModel, Field

from ..categorys.schemas import Category


class ShowAnnouncement(BaseModel):
    id: int
    title: str
    content: str
    category: Category


class CreateAnnouncement(BaseModel):
    author_id: int
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
