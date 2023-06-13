import decimal

import fastapi as fa

from fastapi import Depends
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from services.user.utils.fastapiusers import fastapi_users
from services.payment.utils.robokassa import (
    generate_payment_link,
)
import services.payment.db_handlers as db_hand


async def get_payment_link(
    amount: decimal.Decimal = fa.Body(..., ge=0.01),
    user=Depends(fastapi_users.current_user()),
    session: AsyncSession = fa.Depends(get_async_session),
) -> HttpUrl:
    payment = await db_hand.add_payment(session, user.id, amount)
    url = generate_payment_link(amount, payment.id, user.email)
    return url
