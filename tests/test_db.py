from dataclasses import asdict

from sqlalchemy import select

from app.models import User


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
        'created_at': time,
    }
