from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from services.payment import schemas as payment_schemas
from services.user import models as user_models


Base = declarative_base()


class Payment(Base):
    __tablename__ = "payment"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user = sa.Column(
        sa.Integer,
        sa.ForeignKey(user_models.User.id, name="payment_user_id_fkey"),
        nullable=False,
    )
    action = sa.Column(sa.Enum(payment_schemas.PaymentChoice), nullable=False)
    amount = sa.Column(sa.Integer, nullable=False)
    date = sa.Column(sa.TIMESTAMP, default=datetime.utcnow())
