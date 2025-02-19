import pytest
from fastapi.testclient import TestClient

from app.main import api


@pytest.fixture
def client():
    return TestClient(api)
