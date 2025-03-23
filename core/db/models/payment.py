from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db.mixins import TimestampMixin
from core.db.session import Base


class PaymentModel(Base, TimestampMixin):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Numeric(11, 2, asdecimal=False), nullable=False)
    transaction_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallet.id"))

    user: Mapped['UserModel'] = relationship(
        "UserModel", back_populates="payment", foreign_keys=[user_id]
    )

    wallet: Mapped['WalletModel'] = relationship(
        "WalletModel", back_populates="payment", foreign_keys=[wallet_id]
    )
