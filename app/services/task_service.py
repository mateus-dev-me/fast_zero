from http import HTTPStatus
from typing import Sequence

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.database.models import Task
from app.database.session import get_session
from app.repositories.task_repository import TaskRepository
from app.schemas.tasks import FilterTask, TaskSchema, TaskUpdate


class TaskService:
    def __init__(self, task_repo: TaskRepository) -> None:
        self.task_repo = task_repo

    def create_task(self, task_data: TaskSchema, user_id: int):
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            state=task_data.state,
            user_id=user_id,
        )

        db_task = self.task_repo.create(new_task)
        return db_task

    def list_tasks(
        self, user_id: int, filter_tasks: FilterTask
    ) -> Sequence[Task]:
        filters = {
            'title': filter_tasks.title,
            'description': filter_tasks.description,
            'state': filter_tasks.state,
            'offset': filter_tasks.offset,
            'limit': filter_tasks.limit,
        }

        return self.task_repo.list_tasks(user_id, filters)

    def update_task(self, task_id: int, task_update: TaskUpdate, user_id: int):
        db_task = self.task_repo.get_by_id(task_id, user_id)
        if not db_task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )

        updates = task_update.model_dump(exclude_unset=True)
        task = self.task_repo.update(db_task, updates)
        return task

    def delete_task(self, task_id: int, user_id: int) -> None:
        db_task = self.task_repo.get_by_id(task_id, user_id)
        if not db_task:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
            )
        self.task_repo.delete(db_task)


def get_task_service(session: Session = Depends(get_session)):
    task_repo = TaskRepository(session)
    return TaskService(task_repo)
