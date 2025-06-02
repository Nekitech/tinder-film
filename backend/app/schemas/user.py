from fastapi import Form
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str = Form(),
    password: str = Form(),


# class LoginResponse(BaseModel):
#     code: int = Field(..., description="Status code of the response, e.g., 200 for success")
#     access_token: str = Field(..., description="Generated access token for the user")

class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Generated access token for the user")
