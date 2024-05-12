from app.configs import get_logger
from fastapi import Request
from starlette.concurrency import iterate_in_threadpool

logger = get_logger()


async def logging_middleware(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    logger.info(f"Request Headers: {request.headers}")

    response = await call_next(request)

    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))

    logger.info(f"Response: {response_body[0].decode()}")
    logger.info(f"Response Headers: {dict(response.headers)}\n")

    return response
