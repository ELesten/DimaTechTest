from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.schemas.exceptions_schemas import ExceptionSchema
from app.services.user_service import user_service
from app.api.schemas.user_schema import (
    LoginResponseSchema, LoginSchema
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post(
    "/login",
    response_model=LoginResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Obtaining JWT token",
    description="Endpoint to get JWT authorization token by entering email and password",
    responses={
        status.HTTP_200_OK: {"model": LoginResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
    },
)
async def user_login(login_data: LoginSchema):
    return await user_service.generate_access_token(login_data)


@auth_router.post("/login_docs", include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint for testing via Swagger"""
    login_data = LoginSchema(email=form_data.username, password=form_data.password)
    return await user_service.generate_access_token(login_data)
