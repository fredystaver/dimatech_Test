from fastapi import APIRouter, status

from api.response import GetWalletsResponseSchema
from app.services import WalletService

router = APIRouter(
    prefix="/api/wallets",
    tags=["Wallets"]
)

@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[GetWalletsResponseSchema]
)
async def get_wallets(user_id: int):
    return await WalletService.get_wallets_by_user_id(user_id)
