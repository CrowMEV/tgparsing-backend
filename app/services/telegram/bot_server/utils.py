import asyncio
from datetime import datetime

import fastapi as fa
import httpx
from database.db_async import async_session
from redis.lock import Lock
from services.tariff import db_handlers as tariff_hand
from services.telegram.account import db_handlers as account_hand
from services.telegram.tasks import db_handlers as task_hand
from services.telegram.tasks.models import Task
from services.telegram.tasks.schemas import WorkStatusChoice
from services.user.db_handlers import get_current_by_id
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession
from utils import files
from utils.redis.redis_app import redis_client


async def check_subscribe(session: AsyncSession, user_id: int):
    user_subscribe = await tariff_hand.get_user_subscribe(session, user_id)
    if not user_subscribe or not user_subscribe.active:
        raise fa.HTTPException(
            status_code=403, detail="Your limit has been reached"
        )


async def do_request(route, params: dict):
    with httpx.Client() as client:
        resp = client.post(
            timeout=None, url=f"{config.PARSER_SERVER}{route}", json=params
        )
    print("STATUS CODE", resp.status_code)
    if resp.status_code != 200:
        return WorkStatusChoice.FAILED, None
    return WorkStatusChoice.SUCCESS, resp.json()


async def get_parser_data(session: AsyncSession) -> dict:
    while True:
        accounts = await account_hand.get_tgaccounts(
            session, {"work_status": "FREE"}
        )
        if not accounts:
            await asyncio.sleep(5)
            continue
        account = accounts[0]
        lock_name = f"lock:tgaccount_{account.api_id}"
        lock_inst = redis_client.lock(name=lock_name, blocking=False)
        if not lock_inst.acquire(blocking=False):
            await asyncio.sleep(5)
            continue
        await account_hand.update_tgaccount(
            session=session,
            id_account=account.id,
            data={"work_status": "WORK"},
        )
        return {
            "session_string": account.session_string,
            "lock_inst": lock_inst,
            "tg_account_id": account.id,
        }


async def end_parser(
    session: AsyncSession,
    time_start: datetime,
    task_id: int,
    work_status: WorkStatusChoice,
    id_account: int,
    lock_inst: Lock,
):
    job_finish = datetime.utcnow()
    time_work = datetime.strptime(
        str(job_finish - time_start).split(".", maxsplit=1)[0], "%H:%M:%S"
    )
    await task_hand.update_task(
        session,
        task_id,
        {
            "job_finish": job_finish,
            "time_work": time_work.time(),
            "work_status": work_status,
        },
    )
    await account_hand.update_tgaccount(
        session=session,
        id_account=id_account,
        data={"work_status": "FREE"},
    )
    lock_inst.release()


async def task_checking(
    session: AsyncSession,
    title: str,
    user_id: int,
    rerun: bool,
    task_data: dict,
) -> Task:
    tasks = await task_hand.get_tasks_by_filter(
        session, {"title": title, "user_id": user_id}
    )
    if rerun and tasks:
        task = tasks[0]
        task_data.update({"job_start": datetime.utcnow()})
        await task_hand.update_task(
            session, task_id=task.id, task_data=task_data
        )
    elif not tasks:
        task = await task_hand.create_task(
            session,
            task_data=task_data,
        )
    else:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Задание с таким именем уже существует",
        )
    return task


async def get_members(
    session_string: str,
    parsed_chats: list,
    groups_count: int,
):
    params = {
        "session_string": session_string,
        "parsed_chats": parsed_chats,
        "groups_count": groups_count,
    }
    work_status, result = await do_request("/members", params)
    return work_status, result


async def get_active_members(
    session_string: str,
    parsed_chats: list,
    from_date: str,
    to_date: str,
    activity_count: int,
    activity: dict,
):
    params = {
        "session_string": session_string,
        "parsed_chats": parsed_chats,
        "from_date": from_date,
        "to_date": to_date,
        "activity_count": activity_count,
        "activity": activity,
    }
    work_status, result = await do_request("/activemembers", params)
    return work_status, result


async def get_geo_members(
    session_string: str,
    coordinates: list[dict],
    accuracy_radius: int,
):
    params = {
        "session_string": session_string,
        "coordinates": coordinates,
        "accuracy_radius": accuracy_radius,
    }
    work_status, result = await do_request("/geomembers", params)
    return work_status, result


async def do_parsing(
    parsing_task: str,
    data: dict,
):
    async with async_session() as session:
        time_start = datetime.utcnow()
        parser_data = await get_parser_data(session)
        session_string = parser_data["session_string"]
        dir_name = data.pop("dir_name")
        file_name = data.pop("filename")
        task_id = data.pop("task_id")
        try:
            user = await get_current_by_id(session, dir_name)
            options = user.subscribe.tariff_options.copy()  # type: ignore
            options["parsers_per_day"] = options["parsers_per_day"] - 1
            options["simultaneous_parsing"] = (
                options["simultaneous_parsing"] - 1
            )
            await tariff_hand.update_user_subscribe(
                session, user.id, {"tariff_options": options}  # type: ignore
            )
            functions = {
                "get_members": get_members,
                "get_active_members": get_active_members,
                "get_geo_members": get_geo_members,
            }
            work_status, result = await functions[  # type: ignore
                parsing_task
            ](session_string, **data)
            if result is not None:
                await files.write_data_to_csv_file(
                    data=result,
                    dir_name=dir_name,
                    file_name=file_name,
                )
        except Exception:  # pylint: disable=W0718:
            options["parsers_per_day"] = options["parsers_per_day"] + 1
            work_status = "FAILED"
        finally:
            options["simultaneous_parsing"] = (
                options["simultaneous_parsing"] + 1
            )
            await tariff_hand.update_user_subscribe(
                session, user.id, {"tariff_options": options}  # type: ignore
            )
            await end_parser(
                session=session,
                time_start=time_start,
                task_id=task_id,
                work_status=work_status,  # pylint: disable=E0601:
                id_account=parser_data["tg_account_id"],
                lock_inst=parser_data["lock_inst"],
            )
