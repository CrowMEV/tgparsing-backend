import fastapi as fa
import httpx
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from services.telegram.account import db_handlers as account_hand
from services.telegram.member import db_handlers as member_hand
from settings import config


async def get_members(
    account_id: int,
    parsed_chats: list = fa.Query(),
    session: AsyncSession = fa.Depends(get_async_session),
) -> fa.Response:
    account = await account_hand.get_tgaccount_by_id(session, account_id)
    with httpx.Client() as cl:
        resp = cl.get(
            timeout=None,
            url=f"{config.PARSER_SERVER}/members",
            params={
                "session_string": account.session_string,
                "parsed_chats": parsed_chats
            }
        )
    resp_data = resp.json()
    # save to database
    # for item in resp_data:
    #     chat_data, members_data = item.values()
    #     chat = await member_hand.get_chat_by_username(
    #         session, chat_data.get("username")
    #     )
    #     if not chat:
    #         await member_hand.create_chat(session, chat_data)
    #         chat = await member_hand.get_chat_by_username(
    #             session, chat_data.get("username")
    #         )
    #     for member_item in members_data:
    #         member = await member_hand.get_member_by_username(
    #             session, member_item.get("username")
    #         )
    #         if not member:
    #             member = await member_hand.create_member(
    #                 session, member_item
    #             )
    #         if member not in chat.members:
    #             chat.members.append(member)

    # save to file

    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"}
    )


async def get_members_by_geo(
    account_id: int,
    latitude: float,
    longitude: float,
    accuracy_radius: int = fa.Query(description="In meters"),
    session: AsyncSession = fa.Depends(get_async_session),
):
    account = await account_hand.get_tgaccount_by_id(session, account_id)
    with httpx.Client() as cl:
        resp = cl.get(
            timeout=None,
            url=f"{config.PARSER_SERVER}/geomembers",
            params={
                "account_id": account_id,
                "latitude": latitude,
                "longitude": longitude,
                "accuracy_radius": accuracy_radius,
                "session_string": account.session_string,
            }
        )
    if resp.status_code != 200:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail=resp.text
        )
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"}
    )

