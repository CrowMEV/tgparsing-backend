from sqlalchemy.ext.asyncio import AsyncSession

import services.payment.db_handlers as db_hand
import services.payment.schemas as payment_schemas


async def calculate_balance(
    session: AsyncSession,
    user_id: int,
) -> int:
    filter_data = {
        "user": user_id,
        "status": True,
    }
    payments = await db_hand.get_payments(session, filter_data)
    if not payments:
        return 0
    balance = sum(
        payment.amount
        if payment.action == payment_schemas.PaymentChoice.DEBIT
        else -payment.amount
        for payment in payments
    )
    return int(balance)


async def is_purchasable(
    session: AsyncSession,
    data: dict,
) -> bool:
    balance = await calculate_balance(session, data["user"]) or 0
    return balance >= data["price"]
