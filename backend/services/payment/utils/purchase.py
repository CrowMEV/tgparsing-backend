import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession

import services.payment.db_handlers as db_hand
import services.payment.schemas as payment_schemas
from database.db_async import get_async_session


async def make_purchase(
    data: dict,
    session: AsyncSession = fa.Depends(get_async_session),
) -> dict[str, str]:
    payment_data = {
        "user": data["user"],
        "amount": data["amount"],
        "total": data["total"],
        "action": payment_schemas.PaymentChoice.CREDIT,
        "status": True,
    }
    await db_hand.add_payment(session, payment_data)
    return {"detail": "Покупка совершена"}
