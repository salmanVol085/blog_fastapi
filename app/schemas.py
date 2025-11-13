# app/schemas.py
from pydantic import BaseModel, EmailStr

from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int
    author: UserOut
    created_at: datetime
    updated_at: Optional[datetime]
    likes_count: int = 0
    comments_count: int = 0
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    user: UserOut
    created_at: datetime
    class Config:
        from_attributes = True
