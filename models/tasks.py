from sqlalchemy import Column, Integer, String, ForeignKey
from util.database import Base
from pydantic import BaseModel
from typing import Optional

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user = Column(Integer, ForeignKey("users.id"))


class TaskSchema(BaseModel):
    name: str
    description: str

class TaskUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None