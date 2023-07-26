from freezegun import freeze_time

from fast_zero.schemas import UserPublic
from fast_zero.security import create_access_token
from tests.factories import UserFactory


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'mateus',
            'email': 'mateus@example.com',
            'password': '1234',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'username': 'mateus',
        'email': 'mateus@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('users')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(session, client):
    users = UserFactory.create_batch(10)
    session.bulk_save_objects(users)
    session.commit()

    user_schema = [
        UserPublic.model_validate(user).model_dump() for user in users
    ]
    response = client.get('/users')
    assert response.json() == {'users': user_schema}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'matheus',
            'email': 'matheus@example.com',
            'password': '1234',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'matheus',
        'email': 'matheus@example.com',
        'id': user.id,
    }


def test_update_user_with_wrong_user(client, user_factory, token):
    response = client.put(
        f'/users/{user_factory.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_unauthorized_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'teste',
            'email': 'test@test.com',
            'password': 'teste',
        },
    )
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Not authenticated',
    }


def test_unauthorized_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_update_user_with_invalid_token(client):
    token = create_access_token({'sub': 'teste@test.com'})
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste',
            'email': 'teste@test.com',
            'password': 'teste',
        },
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


def test_delete_user_with_wrong_user(client, user_factory, token):
    response = client.delete(
        f'/users/{user_factory.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_create_existing_user(client, user):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registed'}


def test_delete_user_with_invalid_token(client):
    token = create_access_token({'sub': 'teste@test.com'})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_delete_user_with_token_expiry(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        token = client.post(
            '/token', data={'username': user.email, 'password': user.password}
        )
    with freeze_time('2023-07-14 12:31:00'):
        response = client.delete(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
        )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}
