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
