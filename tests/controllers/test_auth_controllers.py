from http import HTTPStatus

from freezegun import freeze_time

from app.core.config import Settings
from app.core.security import create_access_token

settings = Settings()


def test_get_token(client, user):
    response = client.post(
        f'{settings.BASE_URL}/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'type_token' in token


def test_jwt_invalid_token(client):
    response = client.get(
        f'{settings.BASE_URL}/users/2',
        headers={'Authorization': 'Bearer token-invalido'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.get(
        f'{settings.BASE_URL}/users/1',
        headers={'Authorzation': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        f'{settings.BASE_URL}/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_expired_after_time(client, user):
    with freeze_time('2025-02-24 12:00:00'):
        response = client.post(
            f'{settings.BASE_URL}/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-02-24 12:31:00'):
        response = client.put(
            f'{settings.BASE_URL}/users/{user.id}',
            headers={'Authorizatio': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'wrong@wrong.com': '',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}


def test_token_inexistent_user(client):
    response = client.post(
        f'{settings.BASE_URL}/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(client, user):
    response = client.post(
        f'{settings.BASE_URL}/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, user, token):
    response = client.post(
        f'{settings.BASE_URL}/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'type_token' in data
    assert data['type_token'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            f'{settings.BASE_URL}/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            f'{settings.BASE_URL}/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
