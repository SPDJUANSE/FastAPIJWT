# app/schemas/auth_schema.py
from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    nombre: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
