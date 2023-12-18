from pydantic import BaseModel, ConfigDict, EmailStr, conint
from typing import Optional
from datetime import datetime

#define some schema/pydantic model for request and response validation
class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(UserBase):
    pass

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True #optional field

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner: User

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None #fully optional field

class Vote(BaseModel):
    post_id: int 
    dir: conint(le=1)