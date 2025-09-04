from fastapi import APIRouter, Depends
from starlette import status

from app.api.schemas.exceptions_schemas import ExceptionSchema
from app.api.schemas.wallet_schemas import WalletModelSchema
from app.db.models import User
from app.dependencies import get_current_user
from app.services.wallet_service import wallet_service

wallet_router = APIRouter(
    prefix="/wallet",
    tags=["Wallet"],
)

@wallet_router.get(
    "/my_wallets",
    response_model=list[WalletModelSchema],
    status_code=status.HTTP_200_OK,
    summary="Obtaining all user wallets",
    responses={
        status.HTTP_200_OK: {"model": list[WalletModelSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}
    },
)
async def get_wallets(current_user: User = Depends(get_current_user)):
    return await wallet_service.get_wallets_list(current_user.id)