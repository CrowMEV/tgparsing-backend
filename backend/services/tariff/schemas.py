from typing import Any, Optional

from pydantic import BaseModel, Field


class TariffPostModel(BaseModel):
    name: str
    description: str
    period: str = Field(
        ...,
        regex=r"^([1-5] days|[1-4] weeks|[1-6] months|[1-5] years)$",
    )
    price: int
    options: dict[str, Any]


class TariffPatchModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    period: str = Field(
        ...,
        regex=r"^([1-5] days|[1-4] weeks|[1-6] months|[1-5] years)$",
    )
    price: Optional[int]
    options: Optional[dict[str, Any]]


class TariffResponse(TariffPostModel):
    id: int

    class Config:
        orm_mode: bool = True
