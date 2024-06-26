from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title:str
    body:str
    
class show_user(BaseModel):
    name:str
    email:str

class show_blog(BaseModel):
    title:str
    creator:show_user


class user(BaseModel):
    name:str
    email:str
    password:str


class login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
