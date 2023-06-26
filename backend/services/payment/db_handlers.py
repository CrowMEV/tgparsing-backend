import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.payment.models import Payment


async def add_payment(session: AsyncSession, data: dict) -> Payment:
    payment = Payment(**data)
    session.add(payment)
    await session.commit()
    return payment


async def get_payment(
    session: AsyncSession,
    payment_id: int,
) -> Payment | None:
    stmt = sa.select(Payment).where(Payment.id == payment_id)
    payment = await session.execute(stmt)
    return payment.scalars().first()


async def upd_payment(
    session: AsyncSession, payment_id, data: dict
) -> Payment | None:
    stmt = (
        sa.update(Payment)
        .values(data)
        .returning(Payment)
        .where(Payment.id == payment_id)
    )
    result = await session.execute(stmt)
    payment = result.scalars().first()
    await session.commit()
    return payment
