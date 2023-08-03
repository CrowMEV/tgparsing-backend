from typing import Any, Annotated
from decimal import Decimal
from settings import config

import fastapi as fa
import services.payment.db_handlers as db_hand
import services.payment.schemas as payment_schemas
from database.db_async import get_async_session
from services.payment.utils.robokassa import generate_payment_link, calculate_signature
from services.role.schemas import RoleNameChoice
from services.tariff.db_handlers import get_tariff_by_id
from services.user.dependencies import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession


async def get_payment_link(
    create_schema: payment_schemas.PaymentCreate,
    user=fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    payment_data = {
        "user": user.id,
        "amount": create_schema.amount,
        "action": payment_schemas.PaymentChoice.DEBIT,
    }
    payment = await db_hand.add_payment(session, payment_data)
    url_data = {
        "inv_id": payment.id,
        "amount": create_schema.amount,
        "email": create_schema.email or user.email
    }
    url = generate_payment_link(url_data)
    return url


async def result_callback(
        out_sum: Annotated[Decimal, fa.Form(alias="OutSum")], out_sum2: Annotated[Decimal, fa.Form(alias="out_summ")], inv_id: Annotated[int, fa.Form(alias="InvId")], signature: Annotated[str, fa.Form(alias="SignatureValue")]
) -> Any:
    if out_sum != out_sum2:
        raise fa.HTTPException(status_code=400, detail="Суммы не совпадают")
    signature_2 = calculate_signature(out_sum, inv_id, config.RK_CHECK_PASS_2ND)
    if signature.lower() != signature_2:
        raise fa.HTTPException(status_code=400, detail="Хушы не совпадают")
    return "OK" + str(inv_id)


async def get_payments(
    get_data: payment_schemas.PaymentsGetAll = fa.Depends(),
    session: AsyncSession = fa.Depends(get_async_session),
    user=fa.Depends(get_current_user),
) -> Any:
    data = {
        key: value
        for key, value in get_data.dict().items()
        if value is not None
    }
    if user.role.name == RoleNameChoice.USER:
        data["user"] = user.id
    payments = await db_hand.get_payments(session, data)
    return payments
