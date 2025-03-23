from pydantic import BaseModel


class CreateUserRequestSchema(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None
    email: str
    password: str


class UpdateUserRequestSchema(BaseModel):
    email: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    last_name: str | None = None
    password: str | None = None
