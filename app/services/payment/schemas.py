import datetime
import enum
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import Decimal


class PaymentChoice(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class PaymentCreate(BaseModel):
    amount: Decimal = Field(..., ge=0.1)


class PaymentsGetAll(BaseModel):
    status: Optional[bool]
    period_start: Optional[datetime.date]
    period_end: Optional[datetime.date]
