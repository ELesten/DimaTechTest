from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Model

class Wallet(Model):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


__all__ = ['Wallet']
