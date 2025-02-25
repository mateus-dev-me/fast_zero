from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import TaskState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    type_token: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class TaskSchema(BaseModel):
    title: str
    description: str
    state: TaskState


class TaskPublic(TaskSchema):
    id: int


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
