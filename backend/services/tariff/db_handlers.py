from typing import Sequence

import sqlalchemy as sa
from services.tariff.models import Tariff
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tariffs(session: AsyncSession) -> Sequence[Tariff]:
    stmt = sa.select(Tariff)
    result = await session.execute(stmt)
    tariffs = result.scalars().fetchall()
    return tariffs


async def get_tariff_by_id(
    session: AsyncSession, tariff_id: int
) -> Tariff | None:
    stmt = sa.select(Tariff).where(Tariff.id == tariff_id)
    result = await session.execute(stmt)
    tariff = result.scalars().first()
    return tariff


async def get_tariff_by_name(
    session: AsyncSession, tariff_name: str
) -> Tariff | None:
    stmt = sa.select(Tariff).where(Tariff.name == tariff_name)
    result = await session.execute(stmt)
    tariff = result.scalars().first()
    return tariff


async def create_tariff(session: AsyncSession, data: dict) -> Tariff:
    tariff = Tariff(**data)
    session.add(tariff)
    await session.commit()
    return tariff


async def change_tariff(
    session: AsyncSession, tariff_id: int, data: dict
) -> Tariff | None:
    stmt = (
        sa.update(Tariff)
        .values(**data)
        .returning(Tariff)
        .where(Tariff.id == tariff_id)
    )
    result = await session.execute(stmt)
    tariff: Tariff | None = result.scalars().first()
    await session.commit()
    return tariff


async def delete_tariff_by_id(session: AsyncSession, tariff_id: int) -> None:
    stmt = sa.delete(Tariff).where(Tariff.id == tariff_id)
    await session.execute(stmt)
    await session.commit()
