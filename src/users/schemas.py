from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    username: str = Field(max_length=32, min_length=3)
    email: EmailStr = Field(max_length=256)
    password: str = Field(min_length=8)

    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    admin: bool
    banned: bool

    class Config:
        from_attributes = True


class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    superuser: bool
    admin: bool
    banned: bool

    class Config:
        from_attributes = True


class LoginUser(BaseModel):
    email: EmailStr = Field(max_length=256)
    password: str = Field(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str
