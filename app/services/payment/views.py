from datetime import datetime
from decimal import Decimal
from typing import Annotated, Any

import fastapi as fa
import services.payment.db_handlers as payment_hand
import services.payment.schemas as payment_schemas
from database.db_async import get_async_session
from services.payment.utils.robokassa import (
    calc_signature,
    generate_payment_link,
)
from services.role.schemas import RoleNameChoice
from services.user import db_handlers as user_hand
from services.user.dependencies import get_current_user, get_user_time
from services.user.models import User
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession


async def get_payment_link(
    payment_schema: payment_schemas.PaymentCreate,
    current_user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
    user_datetime: datetime = fa.Depends(get_user_time),
) -> Any:
    payment_data = {
        "user_id": current_user.id,
        "amount": payment_schema.amount,
        "action": payment_schemas.PaymentChoice.DEBIT,
    }
    payment = await payment_hand.add_payment(session, payment_data)
    url = generate_payment_link(
        ticket_id=payment.id,
        amount=payment_schema.amount,
        email=current_user.email,
        user_datetime=user_datetime,
    )
    return url


async def result_callback(
    out_sum: Annotated[Decimal, fa.Form(alias="OutSum")],
    inv_id: Annotated[int, fa.Form(alias="InvId")],
    response_signature: Annotated[str, fa.Form(alias="SignatureValue")],
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    signature = calc_signature(out_sum, inv_id, config.rk_password_2)
    if response_signature.lower() == signature:
        payment = await payment_hand.get_payment_by_id(session, inv_id)
        if payment:
            user = payment.user
            await user_hand.update_user(
                session, user.id, {"balance": user.balance + out_sum}
            )
            await payment_hand.upd_payment(session, inv_id, {"status": True})
            return f"OK{inv_id}"


async def get_payments(
    get_data: payment_schemas.PaymentsGetAll = fa.Depends(),
    session: AsyncSession = fa.Depends(get_async_session),
    user: User = fa.Depends(get_current_user),
) -> Any:
    data = {
        key: value
        for key, value in get_data.dict().items()
        if value is not None
    }
    if user.role.name == RoleNameChoice.USER:
        data["user_id"] = user.id
    payments = await payment_hand.get_payments(session, data)
    return payments
