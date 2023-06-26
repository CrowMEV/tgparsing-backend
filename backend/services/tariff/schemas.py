import enum
from typing import Optional

from pydantic import BaseModel


class TariffPostModel(BaseModel):
    name: str
    description: dict


class TariffPatchModel(BaseModel):
    name: Optional[str]
    description: Optional[dict]


class TariffResponse(TariffPostModel):
    id: int

    class Config:
        orm_mode: bool = True


class TariffLimitChoices(enum.Enum):
    DAY: str = "day"
    WEEK: str = "week"
    MONTH: str = "month"


class TariffLimitPostModel(BaseModel):
    tariff: int
    limitation: TariffLimitChoices
    price: int


class TariffLimitPatchModel(BaseModel):
    tariff: int
    limitation: Optional[TariffLimitChoices]
    price: Optional[int]


class TariffLimitResponse(TariffLimitPostModel):
    id: int

    class Config:
        orm_mode: bool = True
