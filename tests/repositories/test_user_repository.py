from tests.factory import UserFactory


def test_create_user(user_repository):
    """Testa se uma tarefa pode ser criada corretamente."""
    user_data = UserFactory.build()
    created_user = user_repository.create(user_data)

    assert created_user.id is not None
    assert created_user.username == user_data.username


def test_get_user_by_username_or_email(user, user_repository):
    db_user = user_repository.get_by_username_or_email(
        username=user.username, email=user.email
    )
    assert db_user is not None
    assert db_user.username == user.username
    assert db_user.email == user.email


def test_get_user_by_id(user, user_repository):
    db_user = user_repository.get_by_id(user.id)
    assert db_user is not None


def test_list_users(user, user_repository):
    offset = 0
    limit = 100
    db_users = user_repository.list_users(offset, limit)
    assert len(db_users) == 1


def test_update_user(user, user_repository):
    user.username = 'testtest'
    user.email = 'test@mail.com'
    updated_data = user_repository.update(user)
    assert updated_data.username == user.username
    assert updated_data.email == user.email


def test_delete_user(user, user_repository):
    user_repository.delete(user)
    db_user = user_repository.get_by_id(user.id)
    assert db_user is None
