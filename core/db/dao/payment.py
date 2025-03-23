from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import PaymentModel


class PaymentDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(
            self,
            user_id: int,
            wallet_id: int,
            amount: str,
            transaction_id: str
    ) -> PaymentModel:
        payment = PaymentModel(
            user_id=user_id,
            amount=amount,
            wallet_id=wallet_id,
            transaction_id=transaction_id
        )
        self.db.add(payment)
        await self.db.flush()
        return payment

    async def get_payment_by_filters(self, **filters) -> PaymentModel | None:
        query = select(PaymentModel).filter_by(**filters)
        payment = await self.db.execute(query)
        return payment.scalars().one_or_none()

    async def get_payments_by_user_id(self, user_id: int) -> list[PaymentModel]:
        query = select(PaymentModel).where(PaymentModel.user_id == user_id)
        payments = await self.db.execute(query)
        return payments.scalars().all()
