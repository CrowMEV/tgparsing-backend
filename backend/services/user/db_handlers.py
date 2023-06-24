from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.user.models import User


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = sa.select(User)
    result = await session.execute(stmt)
    users = result.scalars().fetchall()
    return users


async def get_current_by_id(
    session: AsyncSession, user_id: int
) -> User | None:
    stmt = sa.select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    users = result.scalars().first()
    return users


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = sa.select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user


async def add_user(session: AsyncSession, data: dict) -> None:
    user = User(**data)
    session.add(user)
    await session.commit()


async def update_user(
    session: AsyncSession, user_id: int, data: dict
) -> User | None:
    stmt = (
        sa.update(User)
        .where(User.id == user_id)
        .values(**data)
        .returning(User)
    )
    result = await session.execute(stmt)
    await session.commit()
    user = result.scalars().first()
    return user
