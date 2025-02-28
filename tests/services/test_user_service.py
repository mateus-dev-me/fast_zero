from app.schemas.users import UserSchema
from tests.factory import UserFactory


def test_create_user(user_service):
    data = UserFactory.build()
    user = UserSchema(
        username=data.username,
        email=data.email,
        password=data.password,
    )
    created_user = user_service.create_user(user)
    assert created_user.username == user.username
    assert created_user.email == user.email


def test_get_user(user, user_service):
    db_user = user_service.get_user(user.id, user)
    assert db_user is not None
    assert db_user.username == user.username


def test_list_users(user, user_service):
    offset = 0
    limit = 1
    users = user_service.list_users(offset, limit)
    assert len(users) == 1


def test_update_user(user, user_service):
    new_data = UserSchema(
        username='testtest',
        email='test@mail.com',
        password='test1234',
    )
    updated_user = user_service.update_user(user.id, new_data, user)
    assert updated_user.username == new_data.username
    assert updated_user.email == new_data.email


def test_delete_user(user, user_service):
    message = user_service.delete_user(user.id, user)
    assert message == {'message': 'User deleted'}
