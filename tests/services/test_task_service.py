from http import HTTPStatus

import pytest
from fastapi import HTTPException

from app.schemas.tasks import FilterTask, TaskSchema, TaskUpdate


def test_create_task(user, task_service):
    task_data = TaskSchema(
        title='New Task',
        description='Desc',
        state='draft',
    )

    created_task = task_service.create_task(task_data, user.id)

    assert created_task.id == 1
    assert created_task.title == 'New Task'


def test_list_tasks(user, task, task_service):
    filters = FilterTask(offset=0, limit=10)
    tasks = task_service.list_tasks(user_id=user.id, filter_tasks=filters)

    assert len(tasks) == 1


def test_update_task(user, task, task_service):
    task_update = TaskUpdate(title='Updated Title')
    updated_task = task_service.update_task(
        task_id=task.id, task_update=task_update, user_id=user.id
    )

    assert updated_task.title == 'Updated Title'


def test_update_task_not_found(user, task_service):
    with pytest.raises(HTTPException) as exc:
        task_service.update_task(
            task_id=1, task_update=TaskUpdate(title='Updated'), user_id=user.id
        )

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == 'Task not found'


def test_delete_task(user, task, task_service):
    task_service.delete_task(task_id=task.id, user_id=user.id)


def test_delete_task_not_found(user, task_service):
    with pytest.raises(HTTPException) as exc:
        task_service.delete_task(task_id=1, user_id=user.id)

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == 'Task not found'
