from typing import Sequence

import sqlalchemy as sa
from services.tariff.models import Tariff, UserSubscribe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session


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


async def create_user_subscribe(
    session: AsyncSession, data: dict
) -> UserSubscribe:
    subscribe = UserSubscribe(**data)
    session.add(subscribe)
    await session.commit()
    return subscribe


async def get_user_subscribe(
    session: AsyncSession, user_id: int
) -> UserSubscribe | None:
    stmt = sa.select(UserSubscribe).where(UserSubscribe.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def update_user_subscribe(
    session: AsyncSession, user_id: int, data: dict
) -> UserSubscribe | None:
    stmt = (
        sa.update(UserSubscribe)
        .values(**data)
        .returning(UserSubscribe)
        .where(UserSubscribe.user_id == user_id)
    )
    result = await session.execute(stmt)
    sub: UserSubscribe | None = result.scalars().first()
    await session.commit()
    return sub


async def update_subscribe_options(
    session: AsyncSession, tariffs_list: Sequence[Tariff]
) -> None:
    for tariff in tariffs_list:
        stmt = (
            sa.update(UserSubscribe)
            .where(UserSubscribe.tariff_id == tariff.id)
            .values(tariff_options=tariff.options)
        )
        await session.execute(stmt)
    await session.commit()


async def get_subscribes(
    session: AsyncSession, filter_data: dict | None = None
) -> Sequence[UserSubscribe]:
    stmt = sa.select(UserSubscribe)
    if filter_data:
        for key, value in filter_data:
            stmt = stmt.where(getattr(UserSubscribe, key) == value)
    result = await session.execute(stmt)
    subs = result.scalars().fetchall()
    return subs


def get_tariffs_sync(session_sync: Session) -> Sequence[Tariff]:
    stmt = sa.select(Tariff)
    result = session_sync.execute(stmt)
    tariffs = result.scalars().fetchall()
    return tariffs


def update_subscribe_options_sync(
    session_sync: Session, tariffs_list: Sequence[Tariff]
) -> None:
    for tariff in tariffs_list:
        stmt = (
            sa.update(UserSubscribe)
            .where(UserSubscribe.tariff_id == tariff.id)
            .values(tariff_options=tariff.options)
        )
        session_sync.execute(stmt)
    session_sync.commit()


def get_subscribes_sync(
    session: Session, filter_data: dict | None = None
) -> Sequence[UserSubscribe]:
    stmt = sa.select(UserSubscribe)
    if filter_data:
        for key, value in filter_data.items():
            stmt = stmt.where(getattr(UserSubscribe, key) == value)
    result = session.execute(stmt)
    subs = result.scalars().fetchall()
    return subs


def update_user_subscribe_sync(
    session: Session, user_id: int, data: dict
) -> UserSubscribe | None:
    stmt = (
        sa.update(UserSubscribe)
        .values(**data)
        .returning(UserSubscribe)
        .where(UserSubscribe.user_id == user_id)
    )
    result = session.execute(stmt)
    sub: UserSubscribe | None = result.scalars().first()
    session.commit()
    return sub
