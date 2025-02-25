from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import Task, User
from app.schemas import (
    FilterTask,
    Message,
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
from app.security import get_current_user

router = APIRouter(prefix='/tasks', tags=['tasks'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TaskPublic)
def create_task(task: TaskSchema, session: Session, current_user: CurrentUser):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=current_user.id,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get('/', response_model=TaskList)
def list_tasks(
    filter_task: Annotated[FilterTask, Query()],
    session: Session,
    current_user: CurrentUser,
):
    query = select(Task).where(Task.user_id == current_user.id)

    if filter_task.title:
        query = query.filter(Task.title.contains(filter_task.title))

    if filter_task.description:
        query = query.filter(
            Task.description.contains(filter_task.description)
        )

    if filter_task.state:
        query = query.filter(Task.state == filter_task.state)

    tasks = session.scalars(
        query.offset(filter_task.offset).limit(filter_task.limit)
    ).all()

    return {'tasks': tasks}


@router.patch('/{task_id:int}', response_model=TaskPublic)
def update_task(
    task_id, task: TaskUpdate, session: Session, user: CurrentUser
):
    db_task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )
    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found',
        )

    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete('/{task_id:int}', response_model=Message)
def delete_task(task_id, session: Session, user: CurrentUser):
    db_task = session.scalar(
        select(Task).where(Task.id == task_id, Task.user_id == user.id)
    )
    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    session.delete(db_task)
    session.commit()
    return {'message': 'Task has been deleted successfully.'}
