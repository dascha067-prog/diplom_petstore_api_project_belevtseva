from pydantic import BaseModel, EmailStr

from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    username: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    phone: Optional[str] = None
    userStatus: Optional[int] = None


class ErrorResponse(BaseModel):
    code: int
    message: str
    type: str
