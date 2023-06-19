import enum

from pydantic import BaseModel


class TariffLimitChoices(enum.Enum):
    DAY: str = "day"
    WEEK: str = "week"
    MONTH: str = "month"


class TariffPostModel(BaseModel):
    name: str
    description: dict


class TariffResponse(TariffPostModel):
    id: int

    class Config:
        orm_mode: bool = True
