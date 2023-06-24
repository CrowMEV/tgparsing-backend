from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.tariff.models import Tariff, TariffLimitPrice


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
    stmt = sa.insert(Tariff).values(**data).returning(Tariff)
    result = await session.execute(stmt)
    tariff: Tariff = result.scalars().first()
    await session.commit()
    return tariff


async def change_tariff(
    session: AsyncSession, tariff_id: int, data: dict
) -> Tariff:
    stmt = (
        sa.update(Tariff)
        .values(**data)
        .returning(Tariff)
        .where(Tariff.id == tariff_id)
    )
    result = await session.execute(stmt)
    tariff = result.scalars().first()
    await session.commit()
    return tariff


async def delete_tariff_by_id(session: AsyncSession, tariff_id: int) -> None:
    await delete_tariff_prices(session, tariff_id)
    stmt = sa.delete(Tariff).where(Tariff.id == tariff_id)
    await session.execute(stmt)
    await session.commit()


# Tariff prices
async def tariff_prices_list(
    session: AsyncSession,
) -> Sequence[TariffLimitPrice]:
    stmt = sa.select(TariffLimitPrice)
    result = await session.execute(stmt)
    prices = result.scalars().fetchall()
    return prices


async def get_tariff_prices(
    session: AsyncSession, tariff_id: int
) -> Sequence[TariffLimitPrice]:
    stmt = sa.select(TariffLimitPrice).where(
        TariffLimitPrice.tariff == tariff_id
    )
    result = await session.execute(stmt)
    tariff_prices = result.scalars().fetchall()
    return tariff_prices


async def get_tariff_price_by_id(
    session: AsyncSession, tariff_limit_id: int
) -> TariffLimitPrice:
    stmt = sa.select(TariffLimitPrice).where(
        TariffLimitPrice.id == tariff_limit_id
    )
    result = await session.execute(stmt)
    tariff_price = result.scalars().first()
    return tariff_price


async def delete_tariff_price(
    session: AsyncSession, tariff_price_id: int
) -> None:
    stmt = sa.delete(TariffLimitPrice).where(
        TariffLimitPrice.id == tariff_price_id
    )
    await session.execute(stmt)
    await session.commit()


async def delete_tariff_prices(session: AsyncSession, tariff_id: int) -> None:
    stmt = sa.delete(TariffLimitPrice).where(
        TariffLimitPrice.tariff == tariff_id
    )
    await session.execute(stmt)
    await session.commit()


async def create_tariff_price(
    session: AsyncSession, data: dict
) -> TariffLimitPrice:
    stmt = (
        sa.insert(TariffLimitPrice).values(**data).returning(TariffLimitPrice)
    )
    result = await session.execute(stmt)
    tariff_limit: TariffLimitPrice = result.scalars().first()
    await session.commit()
    return tariff_limit


async def change_tariff_price(
    session: AsyncSession, tariff_price_id: int, data: dict
) -> TariffLimitPrice:
    stmt = (
        sa.update(TariffLimitPrice)
        .values(**data)
        .returning(TariffLimitPrice)
        .where(TariffLimitPrice.id == tariff_price_id)
    )
    result = await session.execute(stmt)
    tariff_price = result.scalars().first()
    await session.commit()
    return tariff_price
