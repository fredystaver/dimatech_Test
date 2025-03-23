from pydantic import BaseModel


class GetWalletsResponseSchema(BaseModel):
    id: int
    balance: float
