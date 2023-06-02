import asyncio

import pytest
import sqlalchemy.ext.asyncio as sa_asyncio
from httpx import AsyncClient
from sqlalchemy import insert

from database.db_async import get_async_session
from database.models.user_model import Base
from server import app
from settings import config


engine_test = sa_asyncio.create_async_engine(config.test_async_url, echo=True)

async_test_session = sa_asyncio.async_sessionmaker(
    engine_test, class_=sa_asyncio.AsyncSession, expire_on_commit=False
)


async def test_async_session() -> sa_asyncio.AsyncSession:
    async with async_test_session() as session:
        yield session


app.dependency_overrides[get_async_session] = test_async_session


@pytest.fixture(autouse=True, scope="class")
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


@pytest.fixture(autouse=True, scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
