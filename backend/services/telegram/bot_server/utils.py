import fastapi as fa
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from services.telegram.account import db_handlers as account_hand
from settings import config


async def do_request(route, params):
    with httpx.Client() as client:
        resp = client.get(
            timeout=None, url=f"{config.PARSER_SERVER}{route}", params=params
        )
    if resp.status_code != 200:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST, detail=resp.text
        )
    return resp.json()


async def get_session_string(session: AsyncSession, account_id: int) -> str:
    account = await account_hand.get_tgaccount_by_id(session, account_id)
    if not account:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Неверно введен id телеграмм аккаунта "
            "или он не существует.",
        )
    return account.session_string
