import re

from pydantic import BaseModel, field_validator, RootModel

from app.api.exceptions import CustomException


class UserCreateSchema(BaseModel):
    email: str
    password: str
    name: str
    surname: str
    is_admin: bool | None = False

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, value):
            return value
        raise CustomException(
            status_code=422,
            detail="Incorrect e-mail address",
            message="Incorrect e-mail address",
        )


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str


class LoginSchema(BaseModel):
    email: str
    password: str


class LoginInfoSchema(BaseModel):
    id: int
    email: str
    name: str
    surname: str


class UserIdResponseSchema(BaseModel):
    id: int


class UserUpdateSchema(BaseModel):
    email: str | None = None
    password: str | None = None
    name: str | None = None
    surname: str | None = None
    is_admin: bool | None = None


class UserWalletSchema(BaseModel):
    id: int
    balance: float
    user_id: int


class UserWalletsSchema(BaseModel):
    id: int
    email: str
    password: str
    name: str
    surname: str
    is_admin: bool
    wallets: list[UserWalletSchema]


class UserItemSchema(BaseModel):
    User: UserWalletsSchema


class UserListSchema(RootModel):
    root: list[UserItemSchema]
