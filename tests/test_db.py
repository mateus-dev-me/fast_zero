from sqlalchemy import select
from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='test_user', email='test_user@example.com', password='secret'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test_user'))

    assert user.username == 'test_user'


def test_repr_user_model(user):
    assert (
        str(user) == f'User(username={user.username!r}, email={user.email!r})'
    )
