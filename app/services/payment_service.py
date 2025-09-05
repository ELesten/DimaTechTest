from abc import ABC, abstractmethod

from sqlalchemy.exc import IntegrityError

from app.api.exceptions import CustomException
from app.api.schemas.payment_schema import IncomingPaymentSchema, PaymentModelSchema, PaymentDataSchema
from app.core.security import create_signature
from app.db.database import async_session
from app.db.models import User
from app.repositories.payment_repository import payment_repository_factory
from app.repositories.wallet_repository import wallet_repository_factory


class AbstractPaymentService(ABC):

    @staticmethod
    @abstractmethod
    async def verify_signature(payment):
        pass

    @abstractmethod
    async def process_payment(self, payment):
        pass
    
    @abstractmethod
    async def get_payments_list(self, user: User):
        pass


class PaymentService(AbstractPaymentService):

    def __init__(self, payment_repo_factory, wallet_repo_factory):
        self.payment_repository_factory = payment_repo_factory
        self.wallet_repository_factory = wallet_repo_factory

    @staticmethod
    def verify_signature(payment: dict):
        payment_signature = payment.pop("signature")
        compared_signature = create_signature(payment)

        if payment_signature != compared_signature:
            raise CustomException(
                status_code=400,
                detail="Wrong signature",
                message="Wrong signature"
            )

    async def process_payment(self, payment: IncomingPaymentSchema):
        payment = payment.model_dump()
        self.verify_signature(payment)

        account_id = payment['account_id']
        user_id = payment['user_id']
        amount = payment['amount']
        tr_id = payment['transaction_id']

        async with async_session() as session:
            try:
                wallet_repo = self.wallet_repository_factory(session)
                payment_repo = self.payment_repository_factory(session)

                wallet = await wallet_repo.get_one(account_id, user_id)
                wallet = wallet.scalar()

                if not wallet:
                    wallet = await wallet_repo.create_one(account_id, user_id)

                await payment_repo.create_one(amount, tr_id, user_id)

                wallet.balance += amount

                await session.commit()

            except IntegrityError as e:
                detail = "Payment has already been processed"

                if "wallet" in str(e.orig):
                    detail = f"Wallet with id {account_id} has already been exists for another user"

                raise CustomException(
                    status_code=400,
                    detail=detail,
                    message="Failed to process payment"
                )
            except Exception:
                raise CustomException(
                    status_code=400,
                    detail="Failed to process payment",
                    message="Failed to process payment"
                )

    async def get_payments_list(self, user: User) -> list:
        async with async_session() as session:
            payment_repo = self.payment_repository_factory(session)
            payments = await payment_repo.get_list(user.id)

        result = [
            PaymentModelSchema(
                Payment=PaymentDataSchema(id=row.id, amount=row.amount, transaction_id=row.transaction_id)
            ) for row in payments
        ]
        return result


payment_service = PaymentService(payment_repository_factory, wallet_repository_factory)
