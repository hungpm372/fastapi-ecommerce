from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import main_router
from app.middlewares import logging_middleware

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.include_router(main_router)
