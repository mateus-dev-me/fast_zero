from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.models import User
from app.database.session import get_session
from app.schemas.base import FilterPage, Message
from app.schemas.users import UserList, UserPublic, UserSchema
from app.services.user_service import UserService, get_user_service

router = APIRouter()

SessionDB = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ServiceUser = Annotated[UserService, Depends(get_user_service)]


@router.post('/', status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: SessionDB, service: ServiceUser):
    return service.create_user(user)


@router.get('/', response_model=UserList)
def list_users(
    filter_users: Annotated[FilterPage, Query()],
    session: SessionDB,
    current_user: CurrentUser,
    service: ServiceUser,
):
    users = service.list_users(
        offset=filter_users.offset, limit=filter_users.limit
    )
    return {'users': users}


@router.get('/{user_id:int}', response_model=UserPublic)
def detail_user(
    user_id: int,
    session: SessionDB,
    current_user: CurrentUser,
    service: ServiceUser,
):
    return service.get_user(user_id, current_user)


@router.put('/{user_id:int}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: SessionDB,
    current_user: CurrentUser,
    service: ServiceUser,
):
    return service.update_user(user_id, user, current_user)


@router.delete('/{user_id:int}', response_model=Message)
def delete_user(
    user_id: int,
    session: SessionDB,
    current_user: CurrentUser,
    service: ServiceUser,
):
    return service.delete_user(user_id, current_user)
