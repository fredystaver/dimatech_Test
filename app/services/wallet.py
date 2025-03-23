from fastapi import HTTPException, status

from app.services.abstract import AbstractService
from core.db.dao import WalletDAO
from core.db.models import WalletModel
from core.db.session import session


class WalletService(AbstractService):
    @classmethod
    async def get_wallets_by_user_id(cls, user_id: int) -> list[WalletModel]:
        if not await cls.get_user_by_filters(id=user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        async with session() as transaction:
            wallets = await WalletDAO(transaction).get_wallets_by_user_id(user_id)

        return wallets
