from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    name : str 
    email : EmailStr
    password : str
    class config:
        orm_mode = True

class UserOut(BaseModel):
    name : str 
    email : str 
    class config:
        orm_mode = True

class Post(BaseModel):
    id : int 
    title : str 
    content : str 
    published : bool 
    created_at : datetime
    user_id : int 
    owner : UserOut
    class config:
        orm_mode = True
    

class PostCreate(BaseModel):
    title : str 
    content : str 
    published : bool 
    

    

class User(BaseModel):
    name : str 
    email : EmailStr
    password : str
    class config:
        orm_mode = True



class UserLogin(BaseModel):
    email: EmailStr
    password : str

class Token(BaseModel):
    access_token : str 
    token_type : str 

class TokenData(BaseModel):
    id : Optional[int] = None