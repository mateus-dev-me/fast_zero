from fastapi import FastAPI

from app.routers import router as main_router

api = FastAPI(
    title='Task Manager FastAPI',
    description='Rest API for task management written in Python with FastAPI.',
    version='0.1.0',
)
api.include_router(main_router)
