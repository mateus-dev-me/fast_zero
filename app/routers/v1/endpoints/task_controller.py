from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.models import User
from app.database.session import get_session
from app.schemas.base import Message
from app.schemas.tasks import (
    FilterTask,
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
from app.services.task_service import TaskService, get_task_service

router = APIRouter()
SessionDB = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ServiceTask = Annotated[TaskService, Depends(get_task_service)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TaskPublic)
def create_task(
    task: TaskSchema,
    session: SessionDB,
    current_user: CurrentUser,
    service: ServiceTask,
):
    return service.create_task(task, current_user.id)


@router.get('/', response_model=TaskList)
def list_tasks(
    filter_tasks: Annotated[FilterTask, Query()],
    session: SessionDB,
    user: CurrentUser,
    service: ServiceTask,
):
    tasks = service.list_tasks(user.id, filter_tasks)
    return {'tasks': tasks}


@router.patch('/{task_id:int}', response_model=TaskPublic)
def update_task(
    task_id,
    task: TaskUpdate,
    session: SessionDB,
    user: CurrentUser,
    service: ServiceTask,
):
    return service.update_task(task_id, task, user.id)


@router.delete('/{task_id:int}', response_model=Message)
def delete_task(
    task_id, session: SessionDB, user: CurrentUser, service: ServiceTask
):
    service.delete_task(task_id, user.id)
    return {'message': 'Task has been deleted successfully.'}
