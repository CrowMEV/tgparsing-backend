import datetime
import decimal
import enum
from typing import Optional

from pydantic import BaseModel, Field


class PaymentChoice(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class PaymentCreate(BaseModel):
    amount: decimal.Decimal = Field(..., ge=1, decimal_places=2)


class PaymentsGetAll(BaseModel):
    status: Optional[bool]
    period_start: Optional[datetime.date]
    period_end: Optional[datetime.date]
