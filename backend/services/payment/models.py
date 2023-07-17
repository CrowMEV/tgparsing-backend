import decimal
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from services import Base
from services.payment.schemas import PaymentChoice


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    action: Mapped[PaymentChoice]
    amount: Mapped[decimal.Decimal]
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    status: Mapped[bool] = mapped_column(default=False)
