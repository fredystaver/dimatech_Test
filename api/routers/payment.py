from fastapi import APIRouter, status

from api.request import PaymentRequestDepositSchema, GetPaymentsRequestModel
from api.response import DepositWalletResponse
from app.services import PaymentService

router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"]
)

@router.post(
    path="/deposit",
    status_code=status.HTTP_200_OK,
    response_model=DepositWalletResponse
)
async def deposit_wallet(body: PaymentRequestDepositSchema):
    return await PaymentService.deposit_wallet(body)

@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[GetPaymentsRequestModel]
)
async def get_payment_by_user_id(user_id: int):
    return await PaymentService.get_payments_by_user_id(user_id)
