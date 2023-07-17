from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.payment.models import Payment


async def add_payment(session: AsyncSession, data: dict) -> Payment:
    payment = Payment(**data)
    session.add(payment)
    await session.commit()
    return payment


async def upd_payment(session: AsyncSession, payment_id: int) -> Payment:
    stmt = (
        sa.update(Payment)
        .values({"status": True})
        .returning(Payment)
        .where(Payment.id == payment_id)
    )
    result = await session.execute(stmt)
    payment = result.scalars().one()
    await session.commit()
    return payment


async def get_payments(
    session: AsyncSession,
    data: dict,
) -> Sequence[Payment] | None:
    stmt = sa.select(Payment)
    period_start = data.pop("period_start", None)
    period_end = data.pop("period_end", None)
    if period_start and period_end:
        stmt = stmt.where(Payment.date.between(period_start, period_end))
    for key, value in data.items():
        stmt = stmt.where(getattr(Payment, key) == value)
    result = await session.execute(stmt)
    payments = result.scalars().fetchall()
    return payments
