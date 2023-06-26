import decimal
import enum
from typing import Optional

from pydantic import Field, EmailStr, BaseModel


class PaymentChoice(enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class PaymentCreate(BaseModel):
    amount: decimal.Decimal = Field(..., ge=0.01)
    email: Optional[EmailStr]
