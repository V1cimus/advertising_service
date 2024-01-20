from typing import Optional

from pydantic import BaseModel, Field

from users.schemas import ShowUser


class ShowComment(BaseModel):
    id: int
    text: str
    author: ShowUser


class CreateComment(BaseModel):
    text: str = Field(max_length=4096)

    class Config:
        from_attributes = True


class UpdateComment(BaseModel):
    text: Optional[str] = Field(None, max_length=4096)

    class Config:
        from_attributes = True
