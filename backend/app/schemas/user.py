from fastapi import Form
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    username: str = Form(...)
    password: str = Form(...)


class UserOut(UserBase):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str = Form(...)
    password: str = Form(...)


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Generated access token for the user")


class PayloadUser(BaseModel):
    sub: str
    username: str
    iat: int
    exp: int
    type: str
