from abc import ABC, abstractmethod
from sqlalchemy import select, column
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Payment


class AbstractPaymentRepository(ABC):

    @abstractmethod
    async def get_list(self, user_id):
        pass

    @abstractmethod
    async def create_one(self, amount, transaction_id, user_id):
        pass


class PaymentRepository(AbstractPaymentRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, user_id: int):
        stmt = (select(Payment.id, Payment.amount, Payment.transaction_id)
                .where(column("user_id") == user_id))
        return await self.session.execute(stmt)

    async def create_one(self, amount: int | float, transaction_id: str, user_id: int):
        payment = Payment(amount=amount, transaction_id=transaction_id, user_id=user_id)
        self.session.add(payment)

def payment_repository_factory(session: AsyncSession):
    return PaymentRepository(session)
