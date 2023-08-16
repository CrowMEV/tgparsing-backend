import enum
import re
from datetime import date, datetime

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
    status: bool | None = None
    period_start: date | None = None
    period_end: date | None = None
    amount: int | None = None
    action: PaymentChoice | None = None
    user: str | None = None


class ResponsePayments(BaseModel):
    id: int
    email: str
    amount: Decimal
    action: PaymentChoice
    status: bool
    date: datetime
