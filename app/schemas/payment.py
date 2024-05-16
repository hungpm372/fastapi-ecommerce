from pydantic import BaseModel, ConfigDict

from app.models.Payment import PaymentMethod, Status as PaymentStatus


class PaymentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD


class PaymentIn(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    status: PaymentStatus


class PaymentCreate(PaymentBase):
    status: PaymentStatus = PaymentStatus.PENDING
    amount: int
    user_id: int
