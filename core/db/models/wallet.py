from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db.mixins import TimestampMixin
from core.db.session import Base


class WalletModel(Base, TimestampMixin):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    balance: Mapped[float] = mapped_column(Numeric(11, 2, asdecimal=False), default=0)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped['UserModel'] = relationship(
        "UserModel", back_populates="wallets", foreign_keys=[user_id]
    )

    payment: Mapped[list['PaymentModel']] = relationship(
        "PaymentModel", back_populates="wallet"
    )
