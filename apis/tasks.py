from fastapi import status, HTTPException, Depends, APIRouter
from typing import Annotated
from util.database import get_session
from models.user import User
from models.tasks import Task, TaskSchema, TaskUpdateSchema
from sqlalchemy.orm import Session
from apis.auth import get_current_user


router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)
user_dependancy = Annotated[User, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_session)]

@router.post('/')
async def create_task(body: TaskSchema, current_user: user_dependancy, db: db_dependency):
    task = Task(name=body.name, description=body.description, user=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return "task created successfully"

@router.get('/')
async def get_tasks(current_user: user_dependancy, db: db_dependency):
    query = db.query(Task).filter(Task.user == current_user.id).all()
    response = [
        {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "user": {
                'id': current_user.id,
                'username': current_user.id,
                'email': current_user.email
            }
        } for task in query
    ]
    return response


@router.get('/{task_id}/')
async def get_task(task_id: int, current_user: user_dependancy, db: db_dependency):
    task = db.query(Task).filter(Task.user == current_user.id).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    return {
        "id": task.id,
        "name": task.name,
        "description": task.description,
        "user": {
            'id': current_user.id,
            'username': current_user.id,
            'email': current_user.email
        }
    }


@router.post('/{task_id}/')
async def update_task(task_id: int, body: TaskUpdateSchema, current_user: user_dependancy, db: db_dependency):
    task = db.query(Task).filter(Task.user == current_user.id).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    if body.name:
        task.name = body.name
    if body.description:
        task.description = body.description
    db.commit()
    db.refresh(task)
    return "task updated successfully"

@router.delete('/{task_id}/')
async def delete_task(task_id: int, current_user: user_dependancy, db: db_dependency):
    task = db.query(Task).filter(Task.user == current_user.id).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found")
    db.delete(task)
    db.commit()
    return "task deleted successfully"