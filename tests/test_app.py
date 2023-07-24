from fast_zero.schemas import UserPublic
from fast_zero.security import create_access_token


def test_root_dev_retornar_200_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


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
        'id': 1,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.json() == {'users': [user_schema]}


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


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == 200
    assert 'access_token' in token
    assert 'type_token' in token


def test_get_token_with_incorrect_username(client, user):
    response = client.post(
        '/token',
        data={
            'username': 'incorrectusername',
            'password': user.clean_password,
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_with_incorrect_password(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'incorrectpassword'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


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


def test_delete_user_with_invalid_token(client):
    token = create_access_token({'sub': 'teste@test.com'})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}
