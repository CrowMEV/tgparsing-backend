import asyncio
import json
from typing import AsyncGenerator

import pytest
import services.payment.schemas as payment_schemas
import sqlalchemy.ext.asyncio as sa_asyncio
from database.db_async import get_async_session
from httpx import AsyncClient
from server import app
from services import Base
from services.payment.models import Payment
from services.role.models import Role
from services.telegram.account.models import TgAccount
from services.telegram.member.models import Chat, Member
from services.user.models import User
from services.user.utils.security import get_hash_password
from settings import config


engine_test = sa_asyncio.create_async_engine(config.test_async_url, echo=True)

async_test_session = sa_asyncio.async_sessionmaker(
    engine_test, class_=sa_asyncio.AsyncSession, expire_on_commit=False
)


async def test_async_session() -> AsyncGenerator[
    sa_asyncio.AsyncSession, None
]:
    async with async_test_session() as session:
        yield session


@pytest.fixture()
async def get_session() -> AsyncGenerator[sa_asyncio.AsyncSession, None]:
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
    json_file = config.WORK_DIR / "roles_data.json"
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    with json_file.open() as file:
        data = json.load(file)
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


SUPERUSER_PASS = "AFFdmin1%"
SUPERUSER_HASHED_PASSWORD = get_hash_password(SUPERUSER_PASS)
SUPERUSER_EMAIL = "admin@mail.ru"


@pytest.fixture(autouse=True, scope="session")
async def add_superuser(async_client, prepare_database):
    async with async_test_session() as session:
        user = User(
            email=SUPERUSER_EMAIL,
            hashed_password=SUPERUSER_HASHED_PASSWORD,
            firstname="superuser",
            lastname="superuser",
            role_name="ADMIN",
            is_superuser=True,
            is_staff=True,
        )
        session.add(user)
        await session.commit()


@pytest.fixture(scope="function")
async def admin_login(async_client, add_superuser):
    login_url = app.url_path_for(config.USER_LOGIN)
    response = await async_client.post(
        login_url,
        json={
            "email": SUPERUSER_EMAIL,
            "password": SUPERUSER_PASS,
        },
    )
    return response.json()


USER_EMAIL = "155@mail.ru"
USER_PASSWORD = "Hero1721%"


@pytest.fixture(autouse=True, scope="session")
async def add_user(async_client, prepare_database):
    register_url = app.url_path_for(config.USER_REGISTER)
    await async_client.post(
        register_url,
        json={"email": USER_EMAIL, "password": USER_PASSWORD},
    )


@pytest.fixture(scope="function")
async def user_login(async_client, add_user):
    login_url = app.url_path_for(config.USER_LOGIN)
    await async_client.post(
        login_url,
        json={
            "email": USER_EMAIL,
            "password": USER_PASSWORD,
        },
    )


@pytest.fixture(autouse=True, scope="session")
async def add_payments(async_client, add_superuser):
    async with async_test_session() as session:
        payment = Payment(
            user=1,
            amount=1,
            action=payment_schemas.PaymentChoice.DEBIT,
        )
        session.add(payment)
        await session.commit()


@pytest.fixture(autouse=True, scope="session")
async def add_tgaccount(async_client, add_superuser):
    async with async_test_session() as session:
        account = TgAccount(
            api_id=123,
            api_hash="123api12hash",
            phone_number="+79997776644",
            session_string="123session12345",
            work_status="FREE",
            block_status="BLOCK",
        )
        session.add(account)
        await session.commit()


@pytest.fixture(autouse=True, scope="session")
async def add_tgmember_chat(async_client, add_superuser):
    async with async_test_session() as session:
        member_chat = Member(
            user_id=123,
            phone_number="+79997776644",
            first_name="Valera",
            last_name="Sutkin",
            username="valeron133",
            chats=[
                Chat(
                    chat_id=231,
                    title="SAS!!!aSAS",
                    description="Lalala hey",
                    username="oldstars",
                )
            ],
        )
        session.add(member_chat)
        await session.commit()
