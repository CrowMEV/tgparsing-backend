from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from services.user.db_handlers import get_user_by_email
from services.user.models import User
from services.user.utils.cookie import get_cookie_key
from services.user.utils.security import decode_token


async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(get_cookie_key),
) -> User | None:
    data = decode_token(token)
    email = data["email"]
    user = await get_user_by_email(session, email)
    return user
