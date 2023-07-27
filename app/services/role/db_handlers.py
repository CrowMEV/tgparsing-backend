from typing import Sequence

import sqlalchemy as sa
from services.role.models import Role
from sqlalchemy.ext.asyncio import AsyncSession


async def get_role(session: AsyncSession, name: str) -> Role | None:
    stmt = sa.select(Role).where(sa.and_(Role.name == name))
    result = await session.execute(stmt)
    role = result.scalars().first()
    return role


async def get_roles(session: AsyncSession) -> Sequence[Role]:
    stmt = sa.select(Role)
    result = await session.execute(stmt)
    roles = result.scalars().fetchall()
    return roles


async def change_role(session: AsyncSession, data: dict) -> Role | None:
    name = data.pop("name").name
    stmt = (
        sa.update(Role).values(**data).returning(Role).where(Role.name == name)
    )
    result = await session.execute(stmt)
    role = result.scalars().first()
    await session.commit()
    return role
