from datetime import datetime

from pydantic import BaseModel, condecimal


class PaymentRequestDepositSchema(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: condecimal(gt=0)
    signature: str


class GetPaymentsRequestModel(BaseModel):
    id: int
    amount: float
    transaction_id: str
    created_at: datetime
