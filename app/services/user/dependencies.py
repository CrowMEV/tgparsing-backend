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
