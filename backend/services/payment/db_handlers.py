import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from services.payment.models import Payment


async def add_payment(
    session: AsyncSession, data: dict
) -> Payment:

    stmt = (
        sa.insert(Payment)
        .values(**data)
        .returning(Payment)
    )
    payment = await session.execute(stmt)
    await session.commit()
    return payment.scalars().first()


async def get_payment(
    session: AsyncSession, payment_id: int,
) -> Payment | None:
    stmt = sa.select(Payment).where(Payment.id == payment_id)
    payment = await session.execute(stmt)
    return payment.scalars().first()
