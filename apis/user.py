from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated
from apis.auth import get_current_user
from util.database import get_session
from sqlalchemy.orm import Session
from models.user import User


router = APIRouter(
    prefix="/user",
    tags=['user']
)

user_dependancy = Annotated[User, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_session)]

@router.get('/get-profile/')
async def get_profile(current_user: user_dependancy, db: db_dependency):
    return current_user
