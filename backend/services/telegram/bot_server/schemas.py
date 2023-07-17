from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel, Field, validator


class GetChats(BaseModel):
    task_name: str
    query: str = Field(description="Ключевое слово")


class GetMembers(BaseModel):
    task_name: str
    parsed_chats: List[str] = Field(
        min_items=1,
        max_items=5,
        unique_items=True,
        description="Чаты для парсинга",
    )
    groups_count: int = Field(default=1)

    @validator("parsed_chats", pre=True)
    def check_chats(self, value):
        new_value = []
        for item in value:
            new_value.append(item.split("/")[-1])
        return new_value

    @validator("groups_count")
    def check_groups_count(self, value, values):
        if value > len(values["parsed_chats"]):
            raise ValueError(
                "Количество групп не должно превышать "
                "количество переданных чатов."
            )
        return value


class GetActiveMembers(GetMembers):
    from_date: datetime = Field(
        default=datetime.now().replace(microsecond=0) - timedelta(days=1)
    )
    to_date: datetime = Field(default=datetime.now().replace(microsecond=0))


class GetByGeo(BaseModel):
    task_name: str
    latitude: float
    longitude: float
    accuracy_radius: int = Field(description="In meters")
