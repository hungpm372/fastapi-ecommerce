from fastapi import APIRouter

from . import auth
from . import product
from . import order

main_router = APIRouter()
main_router.include_router(auth.router, prefix='/auth', tags=['Authentication'])
main_router.include_router(product.router, prefix='/products', tags=['Product'])
main_router.include_router(order.router, prefix='/orders', tags=['Order'])
