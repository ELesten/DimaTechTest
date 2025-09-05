from fastapi import APIRouter, Depends, Query
from starlette import status

from app.api.schemas.exceptions_schemas import ExceptionSchema
from app.db.models import User
from app.dependencies import get_current_user, is_admin_user
from app.services.user_service import user_service
from app.api.schemas.user_schema import (
    UserCreateSchema, UserUpdateSchema, LoginInfoSchema, UserIdResponseSchema,UserListSchema
)


user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.get(
    "/my_info",
    response_model=LoginInfoSchema,
    status_code=status.HTTP_200_OK,
    summary="Obtaining user information",
    responses={
        status.HTTP_200_OK: {"model": LoginInfoSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
    },
)
async def user_info(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.post(
    "/create",
    response_model=UserIdResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Creating a user(Only for Admin)",
    description="email=unique",
    responses={
        status.HTTP_201_CREATED: {"model": UserIdResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema}
    },
)
async def create_user(user_data: UserCreateSchema, is_admin = Depends(is_admin_user)):
    return await user_service.create_user(user_data)


@user_router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleting a user(Only for Admin)",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema}
    },
)
async def delete_user(pk: int = Query(), is_admin = Depends(is_admin_user)):
    await user_service.delete_user(pk)


@user_router.patch(
    "/update",
    response_model=UserUpdateSchema,
    status_code=status.HTTP_200_OK,
    summary="Updating a user(Only for Admin)",
    responses={
        status.HTTP_200_OK: {"model": UserUpdateSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema}
    },
)
async def update_user(user_data: UserUpdateSchema, pk: int = Query(), is_admin = Depends(is_admin_user)):
    return await user_service.update_user(pk, user_data)


@user_router.get(
    "/users_balances",
    response_model=UserListSchema,
    status_code=status.HTTP_200_OK,
    summary="Obtaining all users and their balances(Only for Admin)",
    responses={
        status.HTTP_200_OK: {"model": UserListSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": ExceptionSchema}
    },
)
async def get_users_balances(is_admin = Depends(is_admin_user)):
    return await user_service.get_user_and_balances_list()
