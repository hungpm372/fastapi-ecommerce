import os
import logging
from fastapi import Request
from starlette.concurrency import iterate_in_threadpool

logs_dir = os.path.join(os.getcwd(), "logs")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, "app.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def logging_middleware(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    logging.info(f"Request Headers: {request.headers}")

    response = await call_next(request)

    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))

    logging.info(f"Response: {response_body[0].decode()}")
    logging.info(f"Response Headers: {dict(response.headers)}\n")

    return response
