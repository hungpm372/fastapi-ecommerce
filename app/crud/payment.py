from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status, HTTPException

from app.models import Payment
from app.models.Payment import Status as PaymentStatus
from app.schemas import PaymentCreate


class PaymentCRUD:
    @staticmethod
    async def create_payment(payment: PaymentCreate, db: AsyncSession):
        new_payment = Payment(**payment.dict())
        db.add(new_payment)
        await db.commit()
        await db.refresh(new_payment)
        return new_payment

    @staticmethod
    async def update_payment_status_by_id(payment_id: int, payment_status: PaymentStatus, db: AsyncSession) -> Payment:
        result = await db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()
        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        payment.status = payment_status
        await db.commit()
        await db.refresh(payment)
        return payment
