import datetime
import decimal
import enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class PaymentChoice(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class PaymentConfirm(BaseModel):
    out_sum: decimal.Decimal
    signature_value: str
    inv_id: int

    @classmethod
    def as_params(
        cls,
        out_sum: decimal.Decimal = Query(..., alias="OutSum"),
        signature_value: str = Query(..., alias="SignatureValue"),
        inv_id: int = Query(..., alias="InvId"),
    ):
        return cls(
            out_sum=out_sum,
            signature_value=signature_value,
            inv_id=inv_id,
        )


class PaymentsGetAll(BaseModel):
    status: Optional[bool] = Field(default=None)
    user: Optional[int] = Field(default=None)
    action: Optional[PaymentChoice] = Field(default=None)
    period_start: Optional[datetime.date] = Field(default=None)
    period_end: Optional[datetime.date] = Field(default=None)


class AddSubscribe(BaseModel):
    tariff_id: int
    autopay: Optional[bool] = Field(default=False)
