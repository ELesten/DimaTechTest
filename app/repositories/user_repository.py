from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select, column, update, RowMapping
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.db.models import User


class AbstractUserRepository(ABC):

    @abstractmethod
    async def get_one(self, search_param, fields):
        pass

    @abstractmethod
    async def create_one(self, user_data):
        pass

    @abstractmethod
    async def delete_one(self, user):
        pass

    @abstractmethod
    async def update_one(self, user_data, user):
        pass

    @abstractmethod
    async def get_list(self):
        pass


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, search_param: tuple, fields: list = None) -> RowMapping | User :
        attr_name, attr_value = search_param

        if fields:
            stmt = select(*(getattr(User, name) for name in fields))
        else:
            stmt = select(User)

        stmt = stmt.where(column(attr_name) == attr_value)

        result = await self.session.execute(stmt)

        return result.mappings().first() if fields else result.scalar()

    async def create_one(self, user_data: dict) -> DeclarativeMeta:
        user = User(**user_data)
        self.session.add(user)
        return user

    async def delete_one(self, user: User):
        await self.session.delete(user)

    async def update_one(self, user_data: dict, user: User) -> User:
        stmt = update(User).where(User.id == user.id).values(**user_data)
        await self.session.execute(stmt)
        return user

    async def get_list(self) -> Sequence[RowMapping]:
        stmt = select(User).options(selectinload(User.wallets))
        result = await self.session.execute(stmt)
        return result.mappings().all()


def user_repository_factory(session: AsyncSession):
    return UserRepository(session)
