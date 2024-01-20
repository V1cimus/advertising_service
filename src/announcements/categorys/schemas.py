from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str


class ShortCategory(BaseModel):
    name: str

    class Config:
        from_attributes = True
