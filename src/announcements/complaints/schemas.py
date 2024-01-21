from datetime import datetime

from pydantic import BaseModel, Field

from ..announcements.schemas import ShowShortAnnouncement


class ShowComplaint(BaseModel):
    id: int
    text: str
    created_at: datetime
    announcement: ShowShortAnnouncement


class CreateComplaint(BaseModel):
    text: str = Field(max_length=4096)

    class Config:
        from_attributes = True
