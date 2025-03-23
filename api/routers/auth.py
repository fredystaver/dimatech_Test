from fastapi import APIRouter, Response, status

from api.request import LoginRequestSchema
from app.services import AuthService

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login(response: Response, body: LoginRequestSchema):
    return await AuthService.login(body=body, response=response)
