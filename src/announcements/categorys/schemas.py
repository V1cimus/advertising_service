from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True
