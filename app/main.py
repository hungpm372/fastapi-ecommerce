from fastapi import FastAPI, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.exceptions import RequestValidationError
from app.configs import get_logger
from app.routers import main_router
from app.middlewares import logging_middleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

logger = get_logger()


# Handling exceptions resource not found
@app.exception_handler(exc_class_or_status_code=status.HTTP_404_NOT_FOUND)
async def resource_not_found_exception_handler(request: Request, exc):
    logger.error(f"Resource not found: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"message": "Resource not found"})


# Handling exceptions unauthorized access
@app.exception_handler(exc_class_or_status_code=status.HTTP_401_UNAUTHORIZED)
async def unauthorized_access_exception_handler(request: Request, exc):
    logger.error(f"Unauthorized access: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"message": "Unauthorized access"})


# Handling exceptions validation error
@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(status_code=400, content={"message": "Validation error", "detail": exc.errors()})


# Include routers
app.include_router(main_router)
