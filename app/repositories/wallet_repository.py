from abc import ABC, abstractmethod

from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from app.db.models import Wallet


class AbstractWalletRepository(ABC):

    @abstractmethod
    async def get_list(self, user_id):
        pass

    @abstractmethod
    async def get_one(self, account_id, user_id):
        pass

    @abstractmethod
    async def create_one(self, account_id, user_id):
        pass


class WalletRepository(AbstractWalletRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, user_id: InstrumentedAttribute[int]) -> Result:
        stmt = select(Wallet.id, Wallet.balance, Wallet.account_id).where(Wallet.user_id == user_id)
        return await self.session.execute(stmt)

    async def get_one(self, account_id: int, user_id: int) -> Result:
        stmt = select(Wallet).where(and_(Wallet.id == account_id, Wallet.user_id == user_id))
        return await self.session.execute(stmt)

    async def create_one(self, account_id: int, user_id: int) -> Wallet:
        wallet = Wallet(user_id=user_id, balance=0, account_id=account_id)
        self.session.add(wallet)
        return wallet


def wallet_repository_factory(session: AsyncSession):
    return WalletRepository(session)
