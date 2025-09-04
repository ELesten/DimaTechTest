from sqlalchemy.exc import IntegrityError

from app.api.exceptions import CustomException
from app.api.schemas.user_schema import LoginSchema, UserUpdateSchema, UserCreateSchema
from app.core.security import verify_password, generate_access_token, hash_password
from app.db.database import async_session
from app.db.models import User
from app.repositories.user_repository import user_repository_factory


class UserService:

    def __init__(self, repository_factory):
        self.user_repository_factory = repository_factory

    async def delete_user(self, pk: int):
        async with async_session() as session:
            user_repo = self.user_repository_factory(session)
            user = await user_repo.get_one(('id', pk))
            if not user:
                raise CustomException(
                    status_code=404,
                    detail=f"User with id {pk} does not exist",
                    message="User not found",
                )
            await user_repo.delete_one(user)
            await session.commit()

    async def update_user(self, pk: int, user_data: UserUpdateSchema) -> User:
        user_data = user_data.model_dump()
        password = user_data.get('password')

        if password:
            user_data['password'] = hash_password(password)

        user_data = {k: v for k, v  in user_data.items() if v is not None}

        async with async_session() as session:
            user_repo = self.user_repository_factory(session)
            user = await user_repo.get_one(('id', pk))

            if user is None:
                raise CustomException(
                    status_code=404,
                    detail=f"User with id {pk} does not exist",
                    message="User not found",
                )

            try:
                updated_user = await user_repo.update_one(user_data, user)
            except IntegrityError:
                raise CustomException(
                    status_code=400,
                    detail="Email must be unique",
                    message="Email already exists"
                )

            await session.commit()

            return updated_user

    async def get_user_info(self, pk: int, fields: list = None) -> User:
        async with async_session() as session:
            user_repo = self.user_repository_factory(session)
            user = await user_repo.get_one(('id', pk), fields=fields)

        if user:
            return user

        raise CustomException(
            status_code=404,
            detail="User with id {pk} does not exist",
            message=f"User not found",
            )

    async def get_user_and_balances_list(self):
        async with async_session() as session:
            user_repo = self.user_repository_factory(session)
            result = await user_repo.get_list()
        return result


    async def generate_access_token(self, login_data: LoginSchema) -> dict:
        email, password = login_data.model_dump().values()

        async with async_session() as session:
            user_repo = self.user_repository_factory(session)
            user = await user_repo.get_one(('email', email))

        if user and verify_password(password, user.password):
            return {"access_token": generate_access_token(user.id), "token_type": "bearer"}

        raise CustomException(
            status_code=404,
            detail="Invalid credentials",
            message="Invalid email or password",
        )

    async def create_user(self, user_data: UserCreateSchema) -> dict:
        user_data = user_data.model_dump()
        user_data['password'] = hash_password(user_data['password'])

        async with async_session() as session:
            user_repo = self.user_repository_factory(session)
            try:
                user = await user_repo.create_one(user_data)
                await session.commit()
                return {'id': user.id}
            except IntegrityError:
                raise CustomException(
                    status_code=400,
                    detail="Email must be unique",
                    message="Email already exists"
                )

user_service = UserService(user_repository_factory)
