from datetime import datetime

from pydantic import BaseModel

from app.database.models import TaskState
from app.schemas.base import FilterPage


class TaskSchema(BaseModel):
    title: str
    description: str
    state: TaskState


class TaskPublic(TaskSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None


class FilterTask(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
