import fastapi as fa
from database.db_async import get_async_session
from fastapi.responses import JSONResponse
from services.telegram.bot_server import schemas as bot_sh
from services.telegram.bot_server import utils
from services.telegram.bot_server.orders import start_parsing
from services.user.dependencies import get_current_user
from services.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_members(
    body_data: bot_sh.GetMembers,
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
) -> fa.Response:
    await utils.check_subscribe(session, current_user.id)
    data = body_data.dict()
    rerun = data.pop("rerun")
    task_name = data.pop("task_name")
    task_data = {
        "title": task_name,
        "user_id": current_user.id,
        "settings": {
            "title": task_name,
            "user_id": current_user.id,
            "parsed_chats": data["parsed_chats"],
            "groups_count": data["groups_count"],
        },
    }
    task = await utils.task_checking(
        session=session,
        title=task_name,
        user_id=current_user.id,
        rerun=rerun,
        task_data=task_data,
    )
    start_parsing.delay(
        "get_members",
        {
            "task_id": task.id,
            "dir_name": current_user.id,
            "filename": body_data.task_name,
            **data,
        },
    )
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг запущен"},
    )


async def get_active_members(
    body_data: bot_sh.GetActiveMembers,
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
) -> fa.Response:
    await utils.check_subscribe(session, current_user.id)
    data = body_data.dict()
    rerun = data.pop("rerun")
    task_name = data.pop("task_name")
    task_data = {
        "title": task_name,
        "user_id": current_user.id,
        "settings": {
            "title": task_name,
            "user_id": current_user.id,
            "parsed_chats": data["parsed_chats"],
            "activity_count": data["activity_count"],
            "activity": data["activity"],
        },
    }
    task = await utils.task_checking(
        session=session,
        title=task_name,
        user_id=current_user.id,
        rerun=rerun,
        task_data=task_data,
    )
    start_parsing.delay(
        "get_active_members",
        {
            "task_id": task.id,
            "dir_name": current_user.id,
            "filename": body_data.task_name,
            **data,
        },
    )
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг запущен"},
    )


async def get_members_by_geo(
    body_data: bot_sh.GetByGeo,
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
):
    await utils.check_subscribe(session, current_user.id)
    data = body_data.dict()
    rerun = data.pop("rerun")
    task_name = data.pop("task_name")
    task_data = {
        "title": task_name,
        "user_id": current_user.id,
        "settings": {
            "title": task_name,
            "user_id": current_user.id,
            "coordinates": data["coordinates"],
            "accuracy_radius": data["accuracy_radius"],
        },
    }
    task = await utils.task_checking(
        session=session,
        title=task_name,
        user_id=current_user.id,
        rerun=rerun,
        task_data=task_data,
    )
    start_parsing.delay(
        "get_geo_members",
        {
            "task_id": task.id,
            "dir_name": current_user.id,
            "filename": body_data.task_name,
            **data,
        },
    )
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Парсинг завершен успешно"},
    )


# TODO: Для парсинга названий чатов по ключевому слову раскомментировать код и
#       обработать ситуацию при которой запись будет происходить при разном
#       объеме данных
# async def get_chats_by_word(
#     body_data: bot_sh.GetChats,
#     session: AsyncSession = fa.Depends(get_async_session),
#     current_user: User = fa.Depends(get_current_user),
# ):
#     await utils.check_task_exists(
#         session=session,
#         title=body_data.task_name,
#         user_id=current_user.id,
#     )
#     time_start = datetime.now()
#     session_string = await utils.get_parser_data(session)
#     params = {
#         "query": body_data.query,
#         "session_string": session_string,
#     }
#     result = await utils.do_request("/chats", params)
#     await utils.write_data_to_file(
#         data=result, dir_name=current_user.email,
#         filename=body_data.task_name
#     )
#     # total_time = datetime.now() - time_start  # pylint: disable=W0612
#     return JSONResponse(
#         status_code=fa.status.HTTP_200_OK,
#         content={"detail": "Парсинг завершен успешно"},
#     )
