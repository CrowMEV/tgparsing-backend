import decimal
from datetime import datetime

import sqlalchemy as sa
from services import Base
from services.payment.schemas import PaymentChoice
from services.user.models import User
from sqlalchemy.orm import Mapped, mapped_column


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    action: Mapped[PaymentChoice]
    amount: Mapped[decimal.Decimal]
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    status: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = sa.orm.relationship(backref="user_payments")
