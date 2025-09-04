from abc import ABC, abstractmethod
from sqlalchemy.orm import InstrumentedAttribute

from app.api.schemas.wallet_schemas import WalletModelSchema, WalletDataSchema
from app.repositories.wallet_repository import  wallet_repository_factory
from app.db.database import async_session

class AbstractWallet(ABC):

    @abstractmethod
    def get_wallets_list(self, user_id):
        pass


class WalletService(AbstractWallet):

    def __init__(self, repository_factory):
        self.wallet_repository_factory = repository_factory

    async def get_wallets_list(self, user_id: InstrumentedAttribute[int]) -> list:
        async with async_session() as session:
            wallet_repo = self.wallet_repository_factory(session)
            wallets = await wallet_repo.get_list(user_id)

        result = [
            WalletModelSchema(Wallet=WalletDataSchema(id=row.id, balance=row.balance)) for row in wallets
        ]
        return result


wallet_service = WalletService(wallet_repository_factory)
