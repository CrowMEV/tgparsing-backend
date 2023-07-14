import decimal

from sqlalchemy.ext.asyncio import AsyncSession

import services.payment.db_handlers as db_hand


async def calculate_balance(
    session: AsyncSession,
    user_id: int,
) -> decimal.Decimal:
    balance = await db_hand.get_balance(session, user_id)
    return decimal.Decimal(balance)
