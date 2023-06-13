import decimal

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from services.payment.models import Payment
from services.payment import schemas as payment_schemas


async def add_payment(
    session: AsyncSession, user: int, amount: decimal.Decimal
):
    action = payment_schemas.PaymentChoice.DEBIT

    stmt = (
        sa.insert(Payment)
        .values(user=user, action=action, amount=amount)
        .returning(Payment)
    )
    payment = await session.execute(stmt)
    await session.commit()
    return payment.scalars().first()
