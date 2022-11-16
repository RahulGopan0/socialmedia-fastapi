from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel): #defining schema using pydantic to make sure the following var are of specific datatype; it does type casting and verfication
    title: str
    content: str
    publish: bool = True
    #Rating: Optional[int] = None

class PostCreate(PostBase): #extension of PostBase schema; basically inheriting content of class PostBase
    pass #just passing contents of PostBase

class PostResponse(PostBase): #To define the response of our api so that we send back only those required info back
    id: int
    user_id: int
    total_votes: int
    created_at: datetime

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel): 
    id: int
    email: EmailStr
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None #it means that if id is given, it is str and if not, then null value; Optional[str] is equivalent to str | None (or Union[str, None]).

