from dataclasses import asdict

from sqlalchemy import select

from app.models import Task, User


def test_create_user_model(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice',
            email='test@mail.com',
            password='1234',
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'email': 'test@mail.com',
        'password': '1234',
        'tasks': [],
        'created_at': time,
        'updated_at': time,
    }


def test_create_task_model(session, user: User):
    task = Task(
        title='test',
        description='testtest',
        state='draft',
        user_id=user.id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)

    assert task in user.tasks
