import datetime

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
    name: str | None
    description: str | None
    limitation_days: int | None
    price: int | None
    options: TariffOptions | None
    active: bool
    archive: bool


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
