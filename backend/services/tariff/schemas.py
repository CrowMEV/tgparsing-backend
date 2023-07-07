from typing import Any, Optional

from pydantic import BaseModel


class TariffPostModel(BaseModel):
    name: str
    description: str
    limitation_days: int
    price: int
    options: dict[str, Any]


class TariffPatchModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    limitation_days: Optional[int]
    price: Optional[int]
    options: Optional[dict[str, Any]]


class TariffResponse(TariffPostModel):
    id: int

    class Config:
        orm_mode: bool = True
