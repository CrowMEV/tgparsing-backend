from typing import Sequence

import sqlalchemy as sa
from services.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session


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


async def get_users_by_filter(
    session: AsyncSession, data: dict
) -> Sequence[User]:
    stmt = sa.select(User)
    if data:
        stmt = stmt.filter_by(**data)
    result = await session.execute(stmt)
    users = result.scalars().fetchall()
    return users


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
    await session.refresh(user)
    return user


def update_user_sync(session: Session, user_id: int, data: dict) -> None:
    stmt = sa.update(User).where(User.id == user_id).values(**data)
    session.execute(stmt)
    session.commit()
