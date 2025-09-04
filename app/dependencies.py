from fastapi import Depends
from sqlalchemy import RowMapping

from app.api.exceptions import CustomException
from app.core.security import verify_access_token
from app.services.user_service import user_service


async def get_current_user(token: dict = Depends(verify_access_token)) -> RowMapping:
    return await user_service.get_user_info(token["id"], fields=["id", "email", "name", "surname"])

async def is_admin_user(token: dict = Depends(verify_access_token)):
    user = await user_service.get_user_info(token['id'])
    if not user.is_admin:
        raise CustomException(
            status_code=403,
            detail="Forbidden",
            message="Permission denied",
        )
