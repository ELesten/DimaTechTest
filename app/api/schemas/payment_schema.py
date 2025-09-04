from pydantic import BaseModel


class PaymentDataSchema(BaseModel):
    id: int
    transaction_id: str
    amount: float


class PaymentModelSchema(BaseModel):
    Payment: PaymentDataSchema


class IncomingPaymentSchema(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: float | int
    signature: str
