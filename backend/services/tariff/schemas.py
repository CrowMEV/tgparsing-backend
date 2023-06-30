from typing import Optional

from pydantic import BaseModel


class TariffPostModel(BaseModel):
    name: str
    description: str
    limitation_days: int
    price: int


class TariffPatchModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    limitation_days: Optional[int]
    price: Optional[int]


class TariffResponse(TariffPostModel):
    id: int

    class Config:
        orm_mode: bool = True


class BenefitRequest(BaseModel):
    name: str


class BenefitResponse(BenefitRequest):
    id: int

    class Config:
        orm_mode: bool = True


class TariffBenefitCreate(BaseModel):
    tariff_id: int
    benefit_id: int


class TariffBenefitResponse(TariffBenefitCreate):
    id: int

    class Config:
        orm_mode: bool = True
