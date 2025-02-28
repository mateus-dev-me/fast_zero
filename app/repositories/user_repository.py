from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import User


class UserRepository:
    """Camada de acesso a dados para usuário."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_username_or_email(
        self, username: str, email: str
    ) -> User | None:
        stmt = select(User).where(
            (User.username == username) | (User.email == email)
        )
        return self.session.scalar(stmt)

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def list_users(self, offset: int, limit: int) -> Sequence[User]:
        stmt = select(User).offset(offset).limit(limit)
        return self.session.scalars(stmt).all()

    def update(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
