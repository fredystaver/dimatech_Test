from pydantic import BaseModel, Field


class WalletSchema(BaseModel):
    id: int
    balance: float


class GetUserResponseSchema(BaseModel):
    id: int
    email: str
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None


class GetUsersResponseSchema(GetUserResponseSchema):
    wallets: list[WalletSchema] | None = None


class CreateUserResponseSchema(BaseModel):
    id: int


class UpdateUserResponseSchema(BaseModel):
    id: int
    email: str
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None
