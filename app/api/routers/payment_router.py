from fastapi import APIRouter, Depends
from starlette import status

from app.api.schemas.exceptions_schemas import ExceptionSchema
from app.api.schemas.payment_schema import PaymentModelSchema, IncomingPaymentSchema
from app.db.models import User
from app.dependencies import get_current_user
from app.services.payment_service import payment_service

payment_router = APIRouter(
    prefix="/payment",
    tags=["Payment"],
)

@payment_router.post(
    "/receive_payment",
    status_code=status.HTTP_200_OK,
    summary="Payment processing",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema}
    }
)
async def payment_handler(payment: IncomingPaymentSchema):
    await payment_service.process_payment(payment)


@payment_router.get(
    "/my_payments",
    response_model=list[PaymentModelSchema],
    status_code=status.HTTP_200_OK,
    summary="Obtaining user payments",
    responses={
        status.HTTP_200_OK: {"model": list[PaymentModelSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}
    }
)
async def get_payments(current_user: User = Depends(get_current_user)):
    return await payment_service.get_payments_list(current_user)
