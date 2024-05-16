from fastapi import APIRouter

from . import auth
from . import product
from . import order
from . import user
from . import payment

main_router = APIRouter()
main_router.include_router(auth.router, prefix='/auth', tags=['Authentication'])
main_router.include_router(user.router, prefix='/users', tags=['User'])
main_router.include_router(product.router, prefix='/products', tags=['Product'])
main_router.include_router(order.router, prefix='/orders', tags=['Order'])
main_router.include_router(payment.router, prefix='/payments', tags=['Payment'])
