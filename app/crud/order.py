from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.payment import PaymentCRUD
from app.crud.product import ProductCRUD
from app.models import Order
from app.models.Order import OrderItem
from app.schemas import OrderCreate, PaymentCreate


class OrderCRUD:

    @staticmethod
    async def create_order(order: OrderCreate, db: AsyncSession, user_id: int) -> Order:
        total_quantity = 0
        total_price = 0
        for order_item in order.order_items:
            product = await ProductCRUD.get_product_by_id(order_item.product_id, db)
            total_quantity += order_item.quantity
            total_price += product.price * order_item.quantity

        # Create order
        new_order = Order(total_quantity=total_quantity, total_price=total_price, address=order.address,
                          phone=order.phone, user_id=user_id)
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)

        await PaymentCRUD.create_payment(
            PaymentCreate(amount=total_price, user_id=user_id, payment_method=order.payment_method), db)

        # Create order items
        items = []
        for order_item in order.order_items:
            items.append(OrderItem(product_id=order_item.product_id, order_id=new_order.id,
                                   quantity=order_item.quantity))
        db.add_all(items)
        await db.commit()
        return new_order
