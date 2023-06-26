from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.payment.models import Payment


async def add_payment(session: AsyncSession, data: dict) -> Payment:
    payment = Payment(**data)
    session.add(payment)
    await session.commit()
    return payment


async def upd_payment(session: AsyncSession, id_row) -> Payment | None:
    data = {"status": True}
    stmt = (
        sa.update(Payment)
        .values(data)
        .returning(Payment)
        .where(Payment.id == id_row)
    )
    result = await session.execute(stmt)
    payment = result.scalars().first()
    await session.commit()
    return payment


def payments_stmt():
    stmt = sa.select(Payment)
    return stmt


async def get_payments(session: AsyncSession) -> Sequence[Payment]:
    stmt = payments_stmt()
    result = await session.execute(stmt)
    payments = result.scalars().fetchall()
    return payments


async def get_payments_by_user_id(
    session: AsyncSession, user_id: int
) -> Sequence[Payment]:
    stmt = payments_stmt()
    stmt = stmt.where(Payment.user == user_id)
    result = await session.execute(stmt)
    payments = result.scalars().fetchall()
    return payments
