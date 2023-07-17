from datetime import datetime, timedelta
from typing import Any

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_sync import Session
from services import Base


def upd_tariff(
    context,
    db_session=Session,
):
    params = context.get_current_parameters()
    tariff_id = params.get("tariff_id")
    with db_session() as session:
        stmt = sa.select(Tariff.limitation_days).where(Tariff.id == tariff_id)
        result = session.execute(stmt)
        days_offset = result.scalars().first()
        return datetime.now() + timedelta(days_offset)


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    limitation_days: Mapped[int]
    price: Mapped[int]
    options: Mapped[dict[str, Any]]


class UserSubscribe(Base):
    __tablename__ = "user_subscribe"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))
    tariff_options: Mapped[dict[str, Any]]
    end_date: Mapped[datetime] = mapped_column(
        default=upd_tariff, onupdate=upd_tariff
    )

    tariff: Mapped["Tariff"] = relationship(backref="users")
