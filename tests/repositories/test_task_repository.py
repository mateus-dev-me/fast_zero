from app.database.models import Task


def test_create_task(user, task_repository):
    task = Task(
        title='Test Task',
        description='Description',
        state='draft',
        user_id=user.id,
    )
    created_task = task_repository.create(task)

    assert created_task.id is not None
    assert created_task.title == 'Test Task'


def test_list_tasks(user, task, task_repository):
    filters = {'title': task.title, 'offset': 0, 'limit': 10}
    tasks = task_repository.list_tasks(user.id, filters=filters)

    assert len(tasks) == 1


def test_get_by_id(user, task, task_repository):
    found_task = task_repository.get_by_id(task.id, user.id)
    assert found_task is not None
    assert found_task.title == task.title


def test_update_task(task, task_repository):
    updates = {'title': 'New Title'}
    updated_task = task_repository.update(task, updates)

    assert updated_task.title == 'New Title'


def test_delete_task(task, task_repository):
    task_repository.delete(task)

    found_task = task_repository.get_by_id(task.id, user_id=1)
    assert found_task is None
