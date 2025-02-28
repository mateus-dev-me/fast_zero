from http import HTTPStatus
from typing import Sequence

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.database.models import User
from app.database.session import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.users import UserPublic, UserSchema


class UserService:
    """Camada de serviços para usuários."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_data: UserSchema) -> UserPublic:
        existing_user = self.user_repo.get_by_username_or_email(
            user_data.username, user_data.email
        )
        if existing_user:
            if existing_user.username == user_data.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists',
                )
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists',
                )

        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
        )
        created_user = self.user_repo.create(user)
        return UserPublic.model_validate(created_user)

    def list_users(self, offset: int, limit: int) -> Sequence[User]:
        return self.user_repo.list_users(offset, limit)

    @staticmethod
    def get_user(user_id: int, current_user: User) -> UserPublic:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permissions',
            )
        return UserPublic.model_validate(current_user)

    def update_user(
        self, user_id: int, user_data: UserSchema, current_user: User
    ) -> UserPublic:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permissions',
            )

        try:
            current_user.username = user_data.username
            current_user.email = user_data.email
            current_user.password = get_password_hash(user_data.password)
            updated_user = self.user_repo.update(current_user)
            return UserPublic.model_validate(updated_user)
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username or Email already exists',
            )

    def delete_user(self, user_id: int, current_user: User) -> dict:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Not enough permissions',
            )
        self.user_repo.delete(current_user)
        return {'message': 'User deleted'}


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    user_repo = UserRepository(session)
    return UserService(user_repo)
