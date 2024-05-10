from fastapi import APIRouter

from . import auth

main_router = APIRouter()
main_router.include_router(auth.router, prefix='/auth', tags=['Authentication'])
