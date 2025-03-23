from pydantic import BaseModel


class DepositWalletResponse(BaseModel):
    balance: float
