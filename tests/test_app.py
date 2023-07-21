from fast_zero.schemas import UserPublic


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


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
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


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')
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


def test_update_user_not_exist(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'teste',
            'email': 'test@test.com',
            'password': 'teste',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_not_exit(client):
    response = client.delete('/users/1')
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
