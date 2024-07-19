from util.database import get_session
from jose import jwt, JWSError
from models.user import User, UserSchema, UserLoginSchema, TokenSchema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_session)]

ALGORITHM = "HS256"
SECRET_KEY = 'secret'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/register/')
async def register(body: UserSchema, db: db_dependency):
    new_user = User(username=body.username, password=pwd_context.hash(body.password), email=body.email, name=body.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return 'user created successfully'


@router.post('/token/')
async def login(form_data: UserLoginSchema, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token(user.username, user.id)
    return {'token': token, 'type': 'bearer', 'username': user.username}


def create_access_token(username: str, user_id: int):
    payload = {
        "sub": username,
        "id": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    if not pwd_context.verify(password, user.password):
        return False

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise JWSError
        return db.query(User).filter(User.username == username).first()
    except JWSError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

