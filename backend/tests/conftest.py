import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

from database.db_async import get_async_session
from database.models.user_model import Base
from server import app
from settings import config


engine_test = create_async_engine(config.test_async_url, echo=True)

async_test_session = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


async def test_async_session() -> AsyncSession:
    async with async_test_session() as session:
        yield session


app.dependency_overrides[get_async_session] = test_async_session


@pytest.fixture(autouse=True, scope='class')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def async_client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
