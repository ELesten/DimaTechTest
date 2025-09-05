from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.core.config import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)

async_engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()

DeclarativeBase = declarative_base(metadata=metadata)


class Model(DeclarativeBase):
    __abstract__ = True
