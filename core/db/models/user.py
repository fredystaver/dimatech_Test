from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.db.mixins import TimestampMixin
from core.db.session import Base


class UserModel(Base, TimestampMixin):
    __tablename__ = "user"

    USER = "0"
    ADMIN = "1"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(default=USER, server_default=USER)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    second_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)

    wallets: Mapped[list['WalletModel']] = relationship(
        "WalletModel", back_populates="user"
    )

    payment: Mapped[list['PaymentModel']] = relationship(
        "PaymentModel", back_populates="user"
    )
