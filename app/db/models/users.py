from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Model
from .wallets import Wallet # noqa



class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    name: Mapped[str]
    surname: Mapped[str]
    wallets: Mapped[list["Wallet"]] = relationship()
    is_admin: Mapped[bool] = mapped_column(default=False)

__all__ = ['User']
