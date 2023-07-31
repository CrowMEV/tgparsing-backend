import csv
from pathlib import Path

from settings import config


async def delete_file(dir_name: str, file_name: str) -> None:
    file_url = await get_file_url(dir_name, file_name)
    if file_url.exists():
        file_url.unlink()


async def get_file_url(dir_url: str, file_name: str) -> Path:
    return config.files_dir_url / dir_url / f"{file_name}.csv"


async def check_folder(dir_name: int) -> str:
    dir_url = config.files_dir_url / str(dir_name)
    if not dir_url.exists():
        dir_url.mkdir()
    return dir_url


async def write_data_to_csv_file(
    data: dict, dir_name: int, file_name: str
) -> None:
    dir_url = await check_folder(dir_name=dir_name)
    file_url = await get_file_url(dir_url=dir_url, file_name=file_name)
    with open(file_url, "w", encoding="utf-8") as file:
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
