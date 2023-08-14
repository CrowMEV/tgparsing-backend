from datetime import date, datetime
from typing import List, Set

from pydantic import BaseModel, Field, field_validator


class GetChats(BaseModel):
    task_name: str = Field(
        min_length=1, pattern="^[А-ЯЁа-яёA-Za-z0-9-_ ]{1,50}$"
    )
    query: str = Field(description="Ключевое слово")


class GetMembers(BaseModel):
    task_name: str = Field(
        min_length=1, pattern="^[А-ЯЁа-яёA-Za-z0-9-_ ]{1,50}$"
    )
    parsed_chats: Set[str] = Field(
        min_items=1,
        max_items=5,
        description="Чаты для парсинга",
    )
    groups_count: int = Field(default=1, ge=1)
    rerun: bool = Field(default=False)

    @field_validator("parsed_chats", mode="before")
    def check_chats(cls, value):  # pylint: disable=E0213
        new_value = []
        for item in value:
            new_value.append(item.split("/")[-1])
        return new_value

    @field_validator("groups_count")
    def check_groups_count(cls, value, values):  # pylint: disable=E0213
        if value > len(values["parsed_chats"]):
            raise ValueError(
                "Количество групп не должно превышать "
                "количество переданных чатов."
            )
        return value


class Activity(BaseModel):
    comments: bool = Field(default=False)
    reposts: bool = Field(default=False)


class GetActiveMembers(BaseModel):
    task_name: str = Field(
        min_length=1, pattern="^[А-ЯЁа-яёA-Za-z0-9-_ ]{1,50}$"
    )
    parsed_chats: Set[str] = Field(
        min_items=1,
        max_items=5,
        description="Чаты для парсинга",
    )
    from_date: date
    to_date: date
    activity_count: int = Field(default=1, ge=1)
    activity: Activity
    rerun: bool = Field(default=False)

    @field_validator("from_date")
    def change_from_date(cls, value):  # pylint: disable=E0213
        return str(datetime.combine(value, datetime.min.time()))

    @field_validator("to_date")
    def change_to_date(cls, value):  # pylint: disable=E0213
        return str(
            datetime.combine(value, datetime.max.time().replace(microsecond=0))
        )

    @field_validator("activity")
    def check_values(cls, value):  # pylint: disable=E0213
        data = value.dict()
        new_data = {key: value for key, value in data.items() if value}
        if new_data:
            return value
        raise ValueError(
            "Activity должно содержать как минимум один ключ с значением True"
        )


class LatLotSchema(BaseModel):
    latitude: float
    longitude: float


class GetByGeo(BaseModel):
    task_name: str = Field(
        min_length=1, pattern="^[А-ЯЁа-яёA-Za-z0-9-_ ]{1,50}$"
    )
    coordinates: List[LatLotSchema] = Field(
        description="Координаты внутри массива "
        "[{latitude: 0.0, longitude: 0.0}]",
        min_items=1,
    )
    accuracy_radius: int = Field(description="In meters")
    rerun: bool = Field(default=False)
