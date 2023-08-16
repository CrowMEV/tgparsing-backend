from typing import Sequence

import services.user.models as user_models
import sqlalchemy as sa
from services.payment.models import Payment
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession


async def add_payment(session: AsyncSession, data: dict) -> Payment:
    payment = Payment(**data)
    session.add(payment)
    await session.commit()
    return payment


async def upd_payment(
    session: AsyncSession, id_row: int, update_data: dict
) -> Payment | None:
    stmt = (
        sa.update(Payment)
        .values(**update_data)
        .returning(Payment)
        .where(Payment.id == id_row)
    )
    result = await session.execute(stmt)
    payment = result.scalars().first()
    await session.commit()
    return payment


async def get_payments(
    session: AsyncSession,
    data: dict,
) -> Sequence[RowMapping] | None:
    stmt = sa.select(
        Payment.id,
        Payment.status,
        Payment.action,
        Payment.amount,
        Payment.date,
        user_models.User.email,
    ).join(user_models.User)
    period_start = data.pop("period_start", None)
    period_end = data.pop("period_end", None)
    user_email = data.pop("user", None)
    if period_start:
        stmt = stmt.where(Payment.date >= period_start)
    if period_end:
        stmt = stmt.where(Payment.date <= period_end)
    if user_email:
        stmt = stmt.where(user_models.User.email == user_email)
    for key, value in data.items():
        stmt = stmt.where(getattr(Payment, key) == value)
    result = await session.execute(stmt)
    payments = result.mappings().fetchall()
    return payments


async def get_payment_by_id(
    session: AsyncSession, id_row: int, status: bool = False
) -> Payment | None:
    stmt = sa.select(Payment).where(
        sa.and_(Payment.id == id_row, Payment.status == status)
    )
    result = await session.execute(stmt)
    payments = result.scalars().first()
    return payments
