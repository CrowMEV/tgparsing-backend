from datetime import datetime

import sqlalchemy as sa

from services import Base
from services.payment import schemas as payment_schemas


class Payment(Base):
    __tablename__ = "payments"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user = sa.Column(
        sa.Integer,
        sa.ForeignKey("users.id", name="payment_user_id_fkey"),
        nullable=False,
    )
    action = sa.Column(sa.Enum(payment_schemas.PaymentChoice), nullable=False)
    amount = sa.Column(sa.Integer, nullable=False)
    date = sa.Column(sa.TIMESTAMP, default=datetime.utcnow())
