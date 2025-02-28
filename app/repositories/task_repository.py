from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Task


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def list_tasks(self, user_id: int, filters: dict) -> Sequence[Task]:
        query = select(Task).where(Task.user_id == user_id)

        if filters.get('title'):
            query = query.filter(Task.title.contains(filters['title']))

        if filters.get('description'):
            query = query.filter(
                Task.description.contains(filters['description'])
            )

        if filters.get('state'):
            query = query.filter(Task.state == filters['state'])

        return self.session.scalars(
            query.offset(filters['offset']).limit(filters['limit'])
        ).all()

    def get_by_id(self, task_id: int, user_id: int) -> Task | None:
        return self.session.scalar(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )

    def update(self, task: Task, updates: dict) -> Task:
        for key, value in updates.items():
            setattr(task, key, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()
