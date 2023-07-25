from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as user_router

main_router = APIRouter()

main_router.include_router(auth_router, tags=['auth'])
main_router.include_router(user_router, prefix='/users', tags=['user'])
