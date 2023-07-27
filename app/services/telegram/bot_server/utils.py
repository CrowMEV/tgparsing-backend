import asyncio
import csv
import os.path
from datetime import datetime

import fastapi as fa
import httpx
from database.db_async import async_session
from redis.lock import Lock
from services.telegram.account import db_handlers as account_hand
from services.telegram.tasks import db_handlers as task_hand
from services.telegram.tasks.schemas import WorkStatusChoice
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession
from utils.redis.redis_app import redis_client


async def do_request(route, params: dict):
    with httpx.Client() as client:
        resp = client.post(
            timeout=None, url=f"{config.PARSER_SERVER}{route}", json=params
        )
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
    file_url: str,
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
            "file_url": file_url,
            "work_status": work_status,
        },
    )
    await account_hand.update_tgaccount(
        session=session,
        id_account=id_account,
        data={"work_status": "FREE"},
    )
    lock_inst.release()


async def check_task_exists(
    session: AsyncSession,
    title: str,
    user_id: int,
):
    task = await task_hand.get_task_by_filter(
        session, {"title": title, "user_id": user_id}
    )
    if task:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Задание с таким именем уже существует",
        )


async def check_folder(name: str) -> str:
    dir_url = os.path.join(config.abs_files_dir_url, name)
    if not os.path.isdir(dir_url):
        os.mkdir(dir_url)
    return dir_url


async def write_data_to_file(data: dict, dir_name: str, filename: str) -> str:
    dir_url = await check_folder(dir_name)
    new_filename = f"{filename}.csv"
    abs_file_url = os.path.join(dir_url, new_filename)
    with open(abs_file_url, "w", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            [
                "user_id",
                "first_name",
                "last_name",
                "username",
                "phone_number",
                "groups",
            ]
        )
        for key, value in data.items():
            firstname = value["first_name"]
            lastname = value["last_name"]
            username = value["username"]
            phone_number = value["phone_number"]
            groups = value["groups"]
            writer.writerow(
                [
                    key,
                    firstname,
                    lastname,
                    username,
                    phone_number,
                    ", ".join(groups),
                ]
            )
    return os.path.join(
        config.STATIC_DIR, config.FILES_DIR, dir_name, new_filename
    )


async def get_members(
    task_id: int,
    parsed_chats: list,
    groups_count: int,
    dir_name: str,
    filename: str,
):
    async with async_session() as session:
        time_start = datetime.utcnow()
        parser_data = await get_parser_data(session)
        params = {
            "session_string": parser_data["session_string"],
            "parsed_chats": parsed_chats,
            "groups_count": groups_count,
        }
        work_status, result = await do_request("/members", params)
        file_url = ""
        if result:
            file_url = await write_data_to_file(
                data=result, dir_name=dir_name, filename=filename
            )
        await end_parser(
            session=session,
            time_start=time_start,
            task_id=task_id,
            work_status=work_status,
            file_url=file_url,
            id_account=parser_data["tg_account_id"],
            lock_inst=parser_data["lock_inst"],
        )


async def get_active_members(
    task_id: int,
    parsed_chats: list,
    from_date: str,
    to_date: str,
    dir_name: str,
    filename: str,
):
    async with async_session() as session:
        time_start = datetime.utcnow()
        parser_data = await get_parser_data(session)
        params = {
            "session_string": parser_data["session_string"],
            "parsed_chats": parsed_chats,
            "from_date": from_date,
            "to_date": to_date,
        }
        work_status, result = await do_request("/activemembers", params)
        file_url = ""
        if result:
            file_url = await write_data_to_file(
                data=result, dir_name=dir_name, filename=filename
            )
        await end_parser(
            session=session,
            time_start=time_start,
            task_id=task_id,
            work_status=work_status,
            file_url=file_url,
            id_account=parser_data["tg_account_id"],
            lock_inst=parser_data["lock_inst"],
        )


async def get_geo_members(
    task_id: int,
    coordinates: list[dict],
    accuracy_radius: int,
    dir_name: str,
    filename: str,
):
    async with async_session() as session:
        time_start = datetime.utcnow()
        parser_data = await get_parser_data(session)
        params = {
            "session_string": parser_data["session_string"],
            "coordinates": coordinates,
            "accuracy_radius": accuracy_radius,
        }
        work_status, result = await do_request("/geomembers", params)
        file_url = ""
        if result:
            file_url = await write_data_to_file(
                data=result, dir_name=dir_name, filename=filename
            )
        await end_parser(
            session=session,
            time_start=time_start,
            task_id=task_id,
            work_status=work_status,
            file_url=file_url,
            id_account=parser_data["tg_account_id"],
            lock_inst=parser_data["lock_inst"],
        )


async def do_parsing(
    parsing_task: str,
    data: dict,
):
    functions = {
        "get_members": get_members,
        "get_active_members": get_active_members,
        "get_geo_members": get_geo_members,
    }
    await functions[parsing_task](**data)  # type: ignore
