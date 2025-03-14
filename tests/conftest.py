from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from app.core.config import Settings
from app.core.security import get_password_hash
from app.database.models import table_registry
from app.database.session import get_session
from app.main import api
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.task_service import TaskService
from app.services.user_service import UserService
from tests.factory import TaskFactory, UserFactory

settings = Settings()


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(api) as client:
        api.dependency_overrides[get_session] = get_session_override
        yield client

    api.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        f'{settings.BASE_URL}/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def task(session, user):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture
def user_repository(session):
    return UserRepository(session)


@pytest.fixture
def task_repository(session):
    return TaskRepository(session)


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)


@pytest.fixture
def task_service(task_repository):
    return TaskService(task_repository)
