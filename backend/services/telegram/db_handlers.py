from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.telegram.models import TgAccount


async def get_tgaccount_by_id(
    session: AsyncSession, account_id: int
) -> TgAccount | None:
    stmt = sa.select(TgAccount).where(TgAccount.id == account_id)
    result = await session.execute(stmt)
    account = result.scalars().first()
    return account


async def get_tgaccount_by_api_id(
    session: AsyncSession, api_id: int
) -> TgAccount | None:
    stmt = sa.select(TgAccount).where(TgAccount.api_id == api_id)
    result = await session.execute(stmt)
    account = result.scalars().first()
    return account


async def get_tgaccounts(
    session: AsyncSession, data: dict
) -> Sequence[TgAccount] | None:
    stmt = sa.select(TgAccount)
    if data:
        stmt = stmt.where(**data)
    result = await session.execute(stmt)
    accounts = result.scalars().fetchall()
    return accounts


async def create_tgaccount(
    session: AsyncSession, account_data: dict
) -> TgAccount:
    account = TgAccount(**account_data)
    session.add(account)
    await session.commit()
    return account


async def update_tgaccount(
    session: AsyncSession, id_account: int, data: dict
) -> TgAccount | None:
    stmt = (
        sa.update(TgAccount)
        .where(TgAccount.id == id_account)
        .values(**data)
        .returning(TgAccount)
    )
    result = await session.execute(stmt)
    account = result.scalars().first()
    await session.commit()
    return account


async def delete_tgaccount(
    session: AsyncSession, acc_id: int
) -> TgAccount | None:
    stmt = (
        sa.delete(TgAccount).where(TgAccount.id == acc_id).returning(TgAccount)
    )
    result = await session.execute(stmt)
    account = result.scalars().first()
    await session.commit()
    return account
