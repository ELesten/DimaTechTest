from pydantic import BaseModel


class WalletDataSchema(BaseModel):
    id: int
    balance: float


class WalletModelSchema(BaseModel):
    Wallet: WalletDataSchema
