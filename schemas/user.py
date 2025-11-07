from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str       

class TokenData(BaseModel):
    email: Optional[str] = None            