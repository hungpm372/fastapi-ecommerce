from fastapi import APIRouter, status, Depends
from app.configs import get_settings, get_db_session
from app.crud.payment import PaymentCRUD
from app.schemas import PaymentUpdate
from app.utils.jwt_utils import get_current_user

settings = get_settings()
router = APIRouter(dependencies=[Depends(get_current_user)])


@router.put("/{payment_id}")
async def update_payment_status_by_id(payment_id: int, payment: PaymentUpdate, session: get_db_session):
    await PaymentCRUD.update_payment_status_by_id(payment_id, payment.status, session)

    return dict(
        message="Payment updated successfully",
        status_code=status.HTTP_200_OK
    )
