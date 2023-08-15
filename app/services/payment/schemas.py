import enum
import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from pydantic.types import Decimal


class PaymentChoice(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class PaymentCreate(BaseModel):
    amount: Decimal = Field(..., ge=0.1)

    @field_validator("amount")
    @classmethod
    def check_amount(cls, amount):
        pattern = r"^[0-9]{1,8}(.[0-9]{1,2})?$"
        if not re.match(pattern, str(amount)):
            raise ValueError("After dot should be one or two symbols")
        return amount


class PaymentsGetAll(BaseModel):
    status: Optional[bool]
    period_start: Optional[date]
    period_end: Optional[date]
