from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import Todo, User


def test_create_user(session: Session):
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


def test_create_todo(session: Session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))
    assert todo in user.todos
