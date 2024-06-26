from pydantic import BaseModel, ConfigDict

from app.models.Payment import PaymentMethod


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    address: str
    phone: str


class OrderCreate(OrderBase):
    order_items: list[OrderItemCreate]
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD


class OrderOut(OrderBase):
    id: int
    user_id: int
    total_quantity: int
    total_price: int
