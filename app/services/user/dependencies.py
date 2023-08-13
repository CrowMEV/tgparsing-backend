from datetime import datetime

import fastapi as fa
from database.db_async import get_async_session
from services.user.db_handlers import get_user_by_email
from services.user.models import User
from services.user.utils.cookie import get_cookie_key
from services.user.utils.security import decode_token
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    session: AsyncSession = fa.Depends(get_async_session),
    token: str = fa.Depends(get_cookie_key),
) -> User | None:
    data = decode_token(token)
    email = data["email"]
    user = await get_user_by_email(session, email)
    return user


async def get_user_time(request: fa.Request) -> datetime:
    x_datetime_value = request.headers.get("X-Datetime")
    if not x_datetime_value:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="We have not got a special header",
        )
    try:
        date = datetime.strptime(x_datetime_value, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError as exc:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    return date
