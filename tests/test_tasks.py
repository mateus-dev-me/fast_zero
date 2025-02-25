from http import HTTPStatus

from app.models import Task, TaskState
from tests.factory import TaskFactory


def test_create_task(client, user, token, mock_db_time):
    with mock_db_time(model=Task) as time:
        response = client.post(
            '/tasks',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': 'test',
                'description': 'testtest',
                'state': 'draft',
            },
        )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'test',
        'description': 'testtest',
        'state': 'draft',
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
    }


def test_list_tasks_should_return_5_tasks(session, client, user, token):
    expected = 5
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/tasks',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['tasks']) == expected


def test_list_tasks_pagination_should_return_2_tasks(
    session, client, user, token
):
    expected = 2
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/tasks/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['tasks']) == expected


def test_list_task_filter_title_should_return_5_tasks(
    session, user, client, token
):
    expected = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        '/tasks/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected


def test_list_tasks_filter_description_should_return_2_tasks(
    session, client, user, token
):
    expected = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5, user_id=user.id, description='testdescription'
        )
    )
    session.commit()

    response = client.get(
        '/tasks/?description=testdescription',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['tasks']) == expected


def test_list_tasks_filter_state_should_return_5_tasks(
    session, user, client, token
):
    expected = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, state=TaskState.draft)
    )
    session.commit()

    response = client.get(
        '/tasks/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected


def test_list_tasks_filter_combined_should_return_5_todos(
    session, user, client, token
):
    expected = 5
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=TaskState.done,
        )
    )

    session.bulk_save_objects(
        TaskFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TaskState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/tasks/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected


def test_list_task_should_return_all_expected_fields(
    client, session, user, token, mock_db_time
):
    with mock_db_time(model=Task) as time:
        new_task = TaskFactory(user_id=user.id)
        session.add(new_task)
        session.commit()

        response = client.get(
            '/tasks',
            headers={'Authorization': f'Bearer {token}'},
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['tasks'] == [
        {
            'id': 1,
            'title': new_task.title,
            'description': new_task.description,
            'state': new_task.state,
            'created_at': time.isoformat(),
            'updated_at': time.isoformat(),
        },
    ]


def test_task_update_error(client, token):
    response = client.patch(
        '/tasks/10',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'testtask'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_task_update(client, session, user, token):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    session.commit()

    response = client.patch(
        f'/tasks/{task.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'testtask'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'testtask'


def test_delete_task(client, session, user, token):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    session.commit()
    response = client.delete(
        f'/tasks/{task.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_task_error(client, token):
    response = client.delete(
        '/tasks/10', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
