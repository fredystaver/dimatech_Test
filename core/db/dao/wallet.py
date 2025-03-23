from decimal import Decimal

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import WalletModel


class WalletDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_wallets_by_user_id(self, user_id: int) -> list[WalletModel]:
        query = select(WalletModel).where(WalletModel.user_id == user_id)
        wallets = await self.db.execute(query)
        return wallets.scalars().all()

    async def get_wallet_by_filters(self, **filters) -> WalletModel | None:
        query = select(WalletModel).filter_by(**filters)
        wallet = await self.db.execute(query)
        return wallet.scalars().one_or_none()

    async def create_wallet(self, user_id: int) -> WalletModel:
        wallet = WalletModel(user_id=user_id)
        self.db.add(wallet)
        await self.db.flush()
        return wallet

    async def update_balance(self, wallet_id: int, balance: str) -> WalletModel:
        query = update(WalletModel).where(
            WalletModel.id == wallet_id
        ).values(balance=balance).returning(WalletModel)
        result = await self.db.execute(query)
        return result.scalars().first()