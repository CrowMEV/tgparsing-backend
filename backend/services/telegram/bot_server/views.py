import fastapi as fa
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from services.telegram.bot_server import schemas as bot_sh

# from services.telegram.account import db_handlers as account_hand
from services.telegram.bot_server.utils import do_request, get_session_string


# from services.telegram.member import db_handlers as member_hand


async def get_members(
    body_data: bot_sh.GetMembers,
    session: AsyncSession = fa.Depends(get_async_session),
) -> fa.Response:
    session_string = await get_session_string(session, body_data.account_id)
    params = {
        "session_string": session_string,
        "parsed_chats": body_data.parsed_chats,
    }
    await do_request("/members", params)
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
        content={"detail": "Парсинг завершен успешно"},
    )


async def get_active_members(
    body_data: bot_sh.GetActiveMembers,
    session: AsyncSession = fa.Depends(get_async_session),
):
    session_string = await get_session_string(session, body_data.account_id)
    params = {
        "session_string": session_string,
        "parsed_chats": body_data.parsed_chats,
    }
    await do_request("/activemembers", params)
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"},
    )


async def get_members_by_geo(
    body_data: bot_sh.GetByGeo,
    session: AsyncSession = fa.Depends(get_async_session),
):
    session_string = await get_session_string(session, body_data.account_id)
    params = {
        "account_id": body_data.account_id,
        "latitude": body_data.latitude,
        "longitude": body_data.longitude,
        "accuracy_radius": body_data.accuracy_radius,
        "session_string": session_string,
    }
    await do_request("/geomembers", params)
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"},
    )


async def get_chats_by_word(
    body_data: bot_sh.GetChats,
    session: AsyncSession = fa.Depends(get_async_session),
):
    session_string = await get_session_string(session, body_data.account_id)
    params = {
        "query": body_data.query,
        "session_string": session_string,
    }
    await do_request("/chats", params)
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"},
    )
