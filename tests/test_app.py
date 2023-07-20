from fastapi.testclient import TestClient
from fast_zero.app import app

client = TestClient(app)


def test_root_dev_retornar_200_e_ola_mundo():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user():
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


def test_read_users():
    response = client.get('users')
    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {'username': 'mateus', 'email': 'mateus@example.com', 'id': 1}
        ]
    }


def test_update_user():
    response = client.put(
        '/users/1',
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


def test_delete_user():
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}
