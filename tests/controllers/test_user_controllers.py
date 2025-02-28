from http import HTTPStatus

from app.core.config import Settings

settings = Settings()


def test_create_user(client):
    response = client.post(
        f'{settings.BASE_URL}/users/',
        json={
            'username': 'test_username',
            'email': 'test@mail.com',
            'password': 'teste1234',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test_username',
        'email': 'test@mail.com',
        'id': 1,
    }


def test_create_user_with_existing_username_should_fail(client, user):
    response = client.post(
        f'{settings.BASE_URL}/users',
        json={
            'username': user.username,
            'email': 'mateus@mail.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_existing_email_should_fail(client, user):
    response = client.post(
        f'{settings.BASE_URL}/users',
        json={
            'username': 'mateus',
            'email': user.email,
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_list_users_with_users(client, user, token):
    response = client.get(
        f'{settings.BASE_URL}/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': user.username, 'email': user.email}]
    }


def test_detail_user(client, user, token):
    response = client.get(
        f'{settings.BASE_URL}/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': 1,
    }


def test_detail_user_with_wrong_user(client, other_user, token):
    response = client.get(
        f'{settings.BASE_URL}/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user(client, user, token):
    response = client.put(
        f'{settings.BASE_URL}/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test2_username',
            'email': 'test2@mail.com',
            'password': 'test2134',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test2_username',
        'email': 'test2@mail.com',
        'id': 1,
    }


def test_update_user_should_return_forbidden(client, token):
    response = client.put(
        f'{settings.BASE_URL}/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test2_username',
            'email': 'test2@mail.com',
            'password': 'test2134',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, token):
    client.post(
        f'{settings.BASE_URL}/users',
        json={
            'username': 'fausto',
            'email': 'fausto@mail.com',
            'password': '1234',
        },
    )

    response = client.put(
        f'{settings.BASE_URL}/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@mail.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'{settings.BASE_URL}/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@mail.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'{settings.BASE_URL}/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_unauthorized(client):
    response = client.delete(f'{settings.BASE_URL}/users/2')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'{settings.BASE_URL}/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
