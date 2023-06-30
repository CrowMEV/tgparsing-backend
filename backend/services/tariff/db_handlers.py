from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from services.tariff.models import Benefit, Tariff, TariffBenefit


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


# benefits
async def get_benefits(session: AsyncSession) -> Sequence[Benefit]:
    stmt = sa.select(Benefit)
    result = await session.execute(stmt)
    benefits = result.scalars().fetchall()
    return benefits


async def get_benefit_by_id(
    session: AsyncSession, id_row: int
) -> Benefit | None:
    stmt = sa.select(Benefit).where(Benefit.id == id_row)
    result = await session.execute(stmt)
    tariff = result.scalars().first()
    return tariff


async def get_benefit_by_name(
    session: AsyncSession, name: str
) -> Benefit | None:
    stmt = sa.select(Benefit).where(Benefit.name == name)
    result = await session.execute(stmt)
    benefit = result.scalars().first()
    return benefit


async def create_benefit(session: AsyncSession, data: dict) -> Benefit:
    benefit = Benefit(**data)
    session.add(benefit)
    await session.commit()
    return benefit


async def change_benefit(
    session: AsyncSession, benefit_id: int, data: dict
) -> Benefit | None:
    stmt = (
        sa.update(Benefit)
        .values(**data)
        .returning(Benefit)
        .where(Benefit.id == benefit_id)
    )
    result = await session.execute(stmt)
    benefit: Benefit | None = result.scalars().first()
    await session.commit()
    return benefit


async def delete_benefit_by_id(session: AsyncSession, benefit_id: int) -> None:
    stmt = sa.delete(Benefit).where(Benefit.id == benefit_id)
    await session.execute(stmt)
    await session.commit()


# Tariff benefits
async def delete_tariff_benefits(
    session: AsyncSession, tariff_id: int
) -> None:
    stmt = sa.delete(TariffBenefit).where(TariffBenefit.tariff_id == tariff_id)
    await session.execute(stmt)
    await session.commit()


async def tariff_benefits(
    session: AsyncSession, tariff_id: int
) -> Sequence[TariffBenefit]:
    stmt = sa.select(TariffBenefit).where(TariffBenefit.tariff_id == tariff_id)
    result = await session.execute(stmt)
    benefits = result.scalars().fetchall()
    return benefits


async def create_tariff_benefit(
    session: AsyncSession, data: dict
) -> TariffBenefit:
    benefit = TariffBenefit(**data)
    session.add(benefit)
    await session.commit()
    return benefit


async def get_tariff_benefit(
    session: AsyncSession, tariff_id: int, benefit_id: int
) -> TariffBenefit | None:
    stmt = sa.select(TariffBenefit).where(
        and_(
            TariffBenefit.tariff_id == tariff_id,
            TariffBenefit.benefit_id == benefit_id,
        )
    )
    result = await session.execute(stmt)
    tariff_benefit = result.scalars().first()
    return tariff_benefit


async def get_tariff_benefit_by_id(
    session: AsyncSession, id_row: int
) -> TariffBenefit | None:
    stmt = sa.select(TariffBenefit).where(TariffBenefit.id == id_row)
    result = await session.execute(stmt)
    tariff_benefit = result.scalars().first()
    return tariff_benefit


async def delete_tariff_benefit(session: AsyncSession, id_row: int) -> None:
    stmt = sa.delete(TariffBenefit).where(TariffBenefit.id == id_row)
    await session.execute(stmt)
    await session.commit()
