import fastapi as fa
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session

# from services.telegram.account import db_handlers as account_hand
from services.telegram.bot_server.utils import do_request, get_session_string


# from services.telegram.member import db_handlers as member_hand


async def get_members(
    parsed_chats: list = fa.Query(),
    account_id: int = fa.Query(description="Идентификатор телеграм аккаунта"),
    session: AsyncSession = fa.Depends(get_async_session),
) -> fa.Response:
    session_string = await get_session_string(session, account_id)
    params = {"session_string": session_string, "parsed_chats": parsed_chats}
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


async def get_members_by_geo(
    latitude: float,
    longitude: float,
    account_id: int = fa.Query(description="Идентификатор телеграм аккаунта"),
    accuracy_radius: int = fa.Query(description="In meters"),
    session: AsyncSession = fa.Depends(get_async_session),
):
    session_string = await get_session_string(session, account_id)
    params = {
        "account_id": account_id,
        "latitude": latitude,
        "longitude": longitude,
        "accuracy_radius": accuracy_radius,
        "session_string": session_string,
    }
    await do_request("/geomembers", params)
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"},
    )


async def get_chats_by_word(
    query: str = fa.Query(description="Ключевое слово"),
    account_id: int = fa.Query(description="Идентификатор телеграм аккаунта"),
    session: AsyncSession = fa.Depends(get_async_session),
):
    session_string = await get_session_string(session, account_id)
    params = {
        "query": query,
        "session_string": session_string,
    }
    await do_request("/chats", params)
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"},
    )
