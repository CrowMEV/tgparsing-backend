import csv
import os.path
import time
from datetime import datetime

import fastapi as fa
import httpx
from redis.lock import Lock
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import async_session
from services.telegram.account import db_handlers as account_hand
from services.telegram.tasks import db_handlers as task_hand
from settings import config
from utils.redis.redis_app import redis_client


async def do_request(route, params):
    with httpx.Client() as client:
        resp = client.post(
            timeout=None, url=f"{config.PARSER_SERVER}{route}", json=params
        )
    if resp.status_code != 200:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST, detail=resp.text
        )
    return resp.json()


async def get_parser_data(session: AsyncSession) -> dict:
    while True:
        accounts = await account_hand.get_tgaccounts(
            session, {"work_status": "FREE"}
        )
        if not accounts:
            time.sleep(5)
            continue
        account = accounts[0]
        lock_name = f"lock:tgaccount_{account.api_id}"
        lock_inst = redis_client.lock(name=lock_name, blocking=False)
        if not lock_inst.acquire(blocking=False):
            time.sleep(5)
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
            "work_status": "IN_WAITING",
            "job_finish": job_finish,
            "time_work": time_work.time(),
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
            detail="Задание с таким именем уже существует"
        )


async def check_folder(name: str) -> str:
    dir_url = os.path.join(config.files_dir_url, name)
    if not os.path.isdir(dir_url):
        os.mkdir(dir_url)
    return dir_url


async def write_data_to_file(data: dict, dir_name: str, filename: str) -> None:
    dir_url = await check_folder(dir_name)
    file_url = os.path.join(dir_url, filename)
    with open(f"{file_url}.csv", "w", encoding="utf-8") as file:
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
        result = await do_request("/members", params)
        await write_data_to_file(
            data=result, dir_name=dir_name, filename=filename
        )
        await end_parser(
            session=session,
            time_start=time_start,
            task_id=task_id,
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
        result = await do_request("/activemembers", params)
        await write_data_to_file(
            data=result, dir_name=dir_name, filename=filename
        )
        await end_parser(
            session=session,
            time_start=time_start,
            task_id=task_id,
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
    }
    await functions[parsing_task](**data)
