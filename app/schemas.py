
from pydantic import BaseModel,EmailStr #The pydantic library is used to mantain the data integrity.
from datetime import datetime
from typing import Optional
from fastapi import File,UploadFile

class UserBase(BaseModel):
    name:str
    email:EmailStr
    

class UserCreate(UserBase):
    password:str
    
class UserResponse(UserBase):
    id:int
    created_at:datetime
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    created_at:datetime
    user_id:int
    user:UserResponse
    
    class Config:
        orm_mode = True
    


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    token : str
    token_type : str

class TokenData(BaseModel):
    id:Optional[str] = None

class Vote(BaseModel):
    post_id: int
    vote_dir:int