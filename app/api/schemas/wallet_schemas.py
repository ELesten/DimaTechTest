from pydantic import BaseModel


class WalletDataSchema(BaseModel):
    id: int
    balance: float
    account_id: int


class WalletModelSchema(BaseModel):
    Wallet: WalletDataSchema
