from typing import Optional

from pydantic import BaseModel


class TariffOptions(BaseModel):
    parsing: int
    tasks: int
    geo: bool
    members: bool


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

    class Config:
        orm_mode: bool = True
