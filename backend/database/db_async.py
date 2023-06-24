from typing import AsyncGenerator

import sqlalchemy.ext.asyncio as sq_async

from settings import config

engine = sq_async.create_async_engine(config.async_url, echo=config.DB_ECHO)
async_session = sq_async.async_sessionmaker(
    engine, class_=sq_async.AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[sq_async.AsyncSession, None]:
    async with async_session() as session:
        yield session
