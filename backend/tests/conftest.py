import asyncio
import json

import pytest
import sqlalchemy.ext.asyncio as sa_asyncio
from httpx import AsyncClient
from passlib.context import CryptContext

from database.db_async import get_async_session
from server import app
from services import Base
from services.role.models import Role
from services.user.models import User
from settings import config


engine_test = sa_asyncio.create_async_engine(config.test_async_url, echo=True)

async_test_session = sa_asyncio.async_sessionmaker(
    engine_test, class_=sa_asyncio.AsyncSession, expire_on_commit=False
)


async def test_async_session() -> sa_asyncio.AsyncSession:
    async with async_test_session() as session:
        yield session


app.dependency_overrides[get_async_session] = test_async_session


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database(event_loop):
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    with open("roles_data.json") as file:
        data: dict = json.load(file)
    async with async_test_session() as session:
        for item_data in data:
            role = Role(**item_data)
            session.add(role)
        await session.commit()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


admin_pass = "AFFdmin1%"
admin_hashed_password = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
).hash(admin_pass)
admin_email = "admin@mail.ru"


@pytest.fixture(autouse=True, scope="session")
async def add_admin(async_client, prepare_database):
    async with async_test_session() as session:
        user = User(
            email=admin_email,
            hashed_password=admin_hashed_password,
            firstname="admin",
            lastname="admin",
            role_name="ADMIN",
            is_superuser=True,
            is_staff=True,
        )
        session.add(user)
        await session.commit()


@pytest.fixture(scope="function")
async def admin_login(async_client, add_admin):
    login_url: str = app.url_path_for(config.USER_LOGIN)
    await async_client.post(
        login_url,
        json={
            "email": admin_email,
            "password": admin_pass,
        },
    )


user_email = "155@mail.ru"
user_name = "vasya"
user_surname = "pupkin"
user_password = "Hero1721%"


@pytest.fixture(autouse=True, scope="session")
async def add_user(async_client, prepare_database):
    await async_client.post(
        "/user/register",
        json={
            "email": user_email,
            "firstname": user_name,
            "lastname": user_surname,
            "password": user_password,
        },
    )


@pytest.fixture(scope="function")
async def user_login(async_client, add_user):
    login_url: str = app.url_path_for(config.USER_LOGIN)
    await async_client.post(
        login_url,
        json={
            "email": user_email,
            "password": user_password,
        },
    )
