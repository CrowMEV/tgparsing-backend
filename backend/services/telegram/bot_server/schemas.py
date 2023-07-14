from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel, Field


class GetChats(BaseModel):
    account_id: int = Field(description="Идентификатор телеграм аккаунта")
    query: str = Field(description="Ключевое слово")


class GetMembers(BaseModel):
    account_id: int = Field(description="Идентификатор телеграм аккаунта")
    parsed_chats: List[str] = Field(
        min_items=1,
        max_items=5,
        unique_items=True,
        description="Чаты для парсинга",
    )


class GetActiveMembers(GetMembers):
    days: int = Field(
        ge=1,
        description="Количество дней. Если указан данный параметр, "
        "то период учитываться не будет",
    )
    from_date: datetime = Field(
        default=datetime.now().replace(microsecond=0) - timedelta(days=1)
    )
    to_date: datetime = Field(default=datetime.now().replace(microsecond=0))


class GetByGeo(BaseModel):
    account_id: int = Field(description="Идентификатор телеграм аккаунта")
    latitude: float
    longitude: float
    accuracy_radius: int = Field(description="In meters")
