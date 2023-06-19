import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from services import Base
from services.tariff.schemas import TariffLimitChoices


class Tariff(Base):
    __tablename__ = "tariffs"
    __table_args__ = (UniqueConstraint('name', name='name_unique'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        nullable=False
    )
    description: Mapped[dict] = mapped_column(sa.JSON)


class TariffLimitPrice(Base):
    __tablename__ = "tariff_price"

    id: Mapped[int] = mapped_column(primary_key=True)
    tariff: Mapped[int] = mapped_column(
        sa.ForeignKey("tariffs.id")
    )
    limitation: Mapped[TariffLimitChoices]
    price: Mapped[int]
