from fastapi import FastAPI

from app.routers import router as main_router

api = FastAPI()
api.include_router(main_router)
