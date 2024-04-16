from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


# This is for the response Backend to End User
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        from_attributes = True  


class ForPostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    user: UserOut

    class Config:
        from_attributes = True   


class PostOut(BaseModel):
    Post: ForPostOut
    votes: int

    class Config:
        from_attributes = True

   
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: bool

    # Validation method for Pydantinc, very usefull 
    # dir: int

    # @validator("dir")
    # def validate_dir(cls, v):
    #     if v not in [0, 1]:
    #         raise ValueError("Dir must be either 0 or 1")
    #     return v
    
