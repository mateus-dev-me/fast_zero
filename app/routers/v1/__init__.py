from fastapi import APIRouter

from app.routers.v1.endpoints.auth_controller import router as auth_router
from app.routers.v1.endpoints.task_controller import router as task_router
from app.routers.v1.endpoints.user_controller import router as user_router

router = APIRouter()
router.include_router(auth_router, prefix='/auth', tags=['auth'])
router.include_router(user_router, prefix='/users', tags=['users'])
router.include_router(task_router, prefix='/tasks', tags=['tasks'])
