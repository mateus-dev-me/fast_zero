from fast_zero.models import TodoState
from tests.factories import TodoFactory, UserFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Teste todo',
            'description': 'Desc todo',
            'state': 'draft',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'title': 'Teste todo',
        'description': 'Desc todo',
        'state': 'draft',
    }


def test_list_todos(session, client, user, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 5


def test_list_todos_with_pagination(session, client, user, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == 2


def test_list_todos_with_filter_title(session, client, user, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.commit()

    response = client.get(
        'todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == 5


def test_list_todos_with_filter_description(session, client, user, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='description')
    )
    session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()['todos']) == 5


def test_list_todos_with_filter_state(session, client, user, token):
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft', headers={'Authorization': f'Bearer {token}'}
    )
    assert len(response.json()['todos']) == 5


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(id=1, user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'Task deleted!'}


def test_delete_todo_nonexistent(client, token):
    response = client.delete(
        '/todos/10', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}


def test_delete_todo_from_different_user(session, client, token):
    user = UserFactory(id=20)
    todo = TodoFactory(id=12, user_id=user.id)
    session.add_all([user, todo])
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_patch_todo(client, todo, token):
    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'description': 'alteration',
        },
    )
    assert response.status_code == 200
    assert response.json()['description'] == 'alteration'


def test_path_todo_nonexistent(client, token):
    response = client.patch(
        '/todos/20',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'alguma coisa',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo_from_different_user(session, client, token):
    user = UserFactory(id=10)
    todo = TodoFactory(id=3, user_id=user.id)

    session.add_all([user, todo])
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'alguma coisa',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}
