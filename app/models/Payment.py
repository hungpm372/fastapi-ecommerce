from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from app.models import BaseModel


class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PaymentMethod(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PAYPAL = "PAYPAL"
    BANK_TRANSFER = "BANK_TRANSFER"


class Payment(BaseModel):
    __tablename__ = 'payments'

    amount = Column(Integer, nullable=False)
    status = Column(postgresql.ENUM(Status, create_type=False), nullable=False, default=Status.PENDING)
    payment_method = Column(postgresql.ENUM(PaymentMethod, create_type=False), nullable=False, default=PaymentMethod.CREDIT_CARD)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationship
    user = relationship('User', back_populates='payments')
