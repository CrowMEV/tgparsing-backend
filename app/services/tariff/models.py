from datetime import datetime
from typing import Any

from services import Base
from services.user.models import User
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    limitation_days: Mapped[int]
    price: Mapped[int]
    options: Mapped[dict[str, Any]]
    active: Mapped[bool] = mapped_column(default=True)
    archive: Mapped[bool] = mapped_column(default=False)


class UserSubscribe(Base):
    __tablename__ = "user_subscribe"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))
    tariff_options: Mapped[dict[str, Any]]
    end_date: Mapped[datetime]

    user: Mapped["User"] = relationship(backref="subscribes")
    tariff: Mapped["Tariff"] = relationship(backref="users")
