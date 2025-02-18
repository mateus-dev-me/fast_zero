from http import HTTPStatus

from fastapi.testclient import TestClient

from app.main import api


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(api)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}
