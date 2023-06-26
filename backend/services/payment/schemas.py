import decimal
import enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field


class PaymentChoice(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class PaymentCreate(BaseModel):
    amount: decimal.Decimal = Field(..., ge=0.01)
    email: Optional[EmailStr]


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
