from fastapi import APIRouter, status, HTTPException, Depends
from app.configs import get_settings, get_db_session
from app.crud.order import OrderCRUD
from app.crud.product import ProductCRUD
from app.crud.user import UserCRUD
from app.schemas import OrderCreate, OrderOut
from app.utils.jwt_utils import get_current_user

settings = get_settings()
router = APIRouter()


@router.post("")
async def create_order(order: OrderCreate, session: get_db_session, user_id: int = Depends(get_current_user)):
    user_db = await UserCRUD.get_user_by_id(user_id, session)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if len(order.order_items) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order items cannot be empty")

    for order_item in order.order_items:
        product_db = await ProductCRUD.get_product_by_id(order_item.product_id, session)
        if not product_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        if product_db.stock_quantity < order_item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product stock is not enough")

        product_db.stock_quantity -= order_item.quantity

    new_order = await OrderCRUD.create_order(order, session, user_id)
    print(new_order)
    return dict(
        message="Order created successfully",
        status_code=status.HTTP_200_OK
    )
