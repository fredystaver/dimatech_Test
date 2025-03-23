import hashlib
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.request import PaymentRequestDepositSchema
from app.services.abstract import AbstractService
from core.config import config
from core.db.dao import WalletDAO, PaymentDAO
from core.db.models import WalletModel, PaymentModel
from core.db.session import session


class PaymentService(AbstractService):
    @classmethod
    async def deposit_wallet(cls, body: PaymentRequestDepositSchema) -> WalletModel:
        wallet_to_update = None
        cls.validate_signature(body)
        if not await cls.get_user_by_filters(id=body.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {body.user_id} not found"
            )
        async with session() as transaction:
            try:
                await cls._check_existing_transaction(
                    transaction=transaction, transaction_id=body.transaction_id
                )
                wallets = await WalletDAO(transaction).get_wallets_by_user_id(body.user_id)

                for wallet in wallets:
                    if wallet.id == body.account_id:
                        wallet_to_update = wallet

                if not wallet_to_update:
                    if await WalletDAO(transaction).get_wallet_by_filters(id=body.account_id):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Account id {body.account_id} already taken by another user"
                        )

                    wallet_to_update = await WalletDAO(transaction).create_wallet(body.user_id)

                new_balance = str(Decimal(wallet_to_update.balance) + body.amount)

                await PaymentDAO(transaction).create_payment(
                    wallet_id=wallet_to_update.id,
                    amount=str(body.amount),
                    user_id=body.user_id,
                    transaction_id=body.transaction_id
                )
                wallet = await WalletDAO(transaction).update_balance(wallet_to_update.id, new_balance)
                await transaction.commit()

                return wallet

            except Exception:
                await transaction.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to process deposit"
                )

    @classmethod
    async def _check_existing_transaction(cls, transaction: AsyncSession, transaction_id: str):
        if await PaymentDAO(transaction).get_payment_by_filters(transaction_id=transaction_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tranasction {transaction_id} already processed"
            )

    @classmethod
    async def get_payments_by_user_id(cls, user_id: int) -> list[PaymentModel]:
        if not await cls.get_user_by_filters(id=user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not exist"
            )
        async with session() as transaction:
            return await PaymentDAO(transaction).get_payments_by_user_id(user_id)

    @classmethod
    def validate_signature(cls, body: PaymentRequestDepositSchema):
        generated_signature = cls._generate_signature(body)
        print(generated_signature)
        if body.signature != generated_signature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invliad signature"
            )

    @classmethod
    def _generate_signature(cls, body: PaymentRequestDepositSchema) -> str:
        body_dict = body.model_dump(exclude={"signature"})
        concat_str = "".join(str(value) for key, value in sorted(body_dict.items())) + config.security.secret_key
        return hashlib.sha256(concat_str.encode("utf-8")).hexdigest()
