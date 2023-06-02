from datetime import datetime

import sqlalchemy as sa
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import declarative_base

from settings import config

Base = declarative_base()


payment_type = sa.Enum("debit", "credit", name="user_payment")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    firstname = sa.Column(sa.String, nullable=False)
    lastname = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, default=datetime.utcnow())
    email = sa.Column(
        sa.String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password = sa.Column(sa.String(length=1024), nullable=False)
    avatar_url = sa.Column(sa.String, default=config.base_avatar_url)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    is_verified = sa.Column(sa.Boolean, default=False, nullable=False)


class Payment(Base):
    __tablename__ = "payment"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user = sa.Column(
        sa.Integer,
        sa.ForeignKey("users.id", name="payment_user_id_fkey"),
        nullable=False,
    )
    action = sa.Column("user_action", payment_type, nullable=False)
    # source = sa.Column(sa.Integer, sa.ForeignKey('sources.id'))
    amount = sa.Column(sa.Integer, nullable=False)
    date = sa.Column(sa.TIMESTAMP, default=datetime.utcnow())
