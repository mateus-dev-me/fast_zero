from http import HTTPStatus

from app.security import create_access_token


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
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
        '/users',
        json={
            'username': 'test_user',
            'email': 'mateus@mail.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_existing_email_should_fail(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'mateus',
            'email': 'test@mail.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_list_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_users(client, user):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'test_user', 'email': 'test@mail.com'}]
    }


def test_detail_user(client, user, token):
    response = client.get(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test_user',
        'email': 'test@mail.com',
        'id': 1,
    }


def test_jwt_invalid_token(client):
    response = client.get(
        '/users/2', headers={'Authorization': 'Bearer token-invalido'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.get(
        'users/1', headers={'Authorzation': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
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
        '/users/2',
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
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@mail.com',
            'password': '1234',
        },
    )

    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'fausto@mail.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client, user, token):
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_unauthorized(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'type_token' in token
