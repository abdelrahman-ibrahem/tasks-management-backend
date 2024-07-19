from sqlalchemy import Column, Integer, String
from util.database import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)


class UserSchema(BaseModel):
    name: str
    email: str
    username: str
    password: str



class UserLoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str