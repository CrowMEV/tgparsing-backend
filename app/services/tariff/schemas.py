import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TariffOptions(BaseModel):
    parsers_per_day: int
    simultaneous_parsing: int
    geo: bool
    members: bool
    activity: bool


class TariffPostModel(BaseModel):
    name: str
    description: str
    limitation_days: int
    price: int
    options: TariffOptions
    active: bool
    archive: bool


class TariffPatchModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    limitation_days: Optional[int]
    price: Optional[int]
    options: Optional[TariffOptions]
    active: Optional[bool]
    archive: Optional[bool]


class TariffResponse(TariffPostModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserSubscribe(BaseModel):
    id: int
    user_id: int
    tariff_id: int
    end_date: datetime.datetime
    tariff_options: TariffOptions
    auto_debit: bool


class UserSubscribeResponse(UserSubscribe):
    model_config = ConfigDict(from_attributes=True)
