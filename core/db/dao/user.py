from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db.models import UserModel


class UserDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: UserModel) -> UserModel:
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_user_by_filters(self, **filters) -> UserModel | None:
        query = select(UserModel).filter_by(**filters)
        user = await self.db.execute(query)
        return user.scalars().one_or_none()

    async def get_all_users(self, limit: int, offset: int) -> list[UserModel]:
        query = select(UserModel).options(selectinload(UserModel.wallets)).limit(limit).offset(offset)
        users = await self.db.execute(query)
        return users.scalars().all()

    async def delete_user(self, user_id: int) -> None:
        query = delete(UserModel).where(UserModel.id == user_id)
        await self.db.execute(query)
        await self.db.commit()
