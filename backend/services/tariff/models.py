from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from services import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    period: Mapped[str]
    options: Mapped[dict[str, Any]]
    price: Mapped[int]


class UserSubscribe(Base):
    __tablename__ = "user_subscribe"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    tariff_id: Mapped[int] = mapped_column(ForeignKey("tariffs.id"))
    options: Mapped[dict[str, Any]]
    end_date: Mapped[datetime]
    autopay: Mapped[bool] = mapped_column(default=False)
    # tariff: Mapped["Tariff"] = relationship(backref="users")
