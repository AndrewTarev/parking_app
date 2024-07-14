from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from main import app
from src.core.config import settings
from src.core.database.base import Base
from src.core.database.db_helper import db_helper

test_db = settings.db_url_test

engine = create_async_engine(test_db, echo=True, poolclass=NullPool)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


app.dependency_overrides[db_helper.get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def db_session():
    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client
