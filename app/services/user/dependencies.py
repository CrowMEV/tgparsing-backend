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


class CheckParserOptions:
    def __init__(self, options_keys_msgs: dict):
        self.options_keys_msgs = options_keys_msgs

    def __call__(self, user: User = fa.Depends(get_current_user)):
        for option_key, error_msg in self.options_keys_msgs.items():
            if user.subscribe.tariff_options[option_key] < 1:
                raise fa.HTTPException(status_code=400, detail=error_msg)
