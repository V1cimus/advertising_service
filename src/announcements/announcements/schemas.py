from pydantic import BaseModel

from ..categorys.schemas import ShortCategory


class ShowAnnouncement(BaseModel):
    id: int
    title: str
    content: str
    category: ShortCategory


class CreateAnnouncement(BaseModel):
    author_id: int
    category_id: int
    title: str
    content: str

    class Config:
        from_attributes = True
