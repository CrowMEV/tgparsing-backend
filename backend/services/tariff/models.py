import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    limitation_days: Mapped[int]
    price: Mapped[int]

    benefits: Mapped[list["TariffBenefit"]] = relationship(
        back_populates="tariff"
    )


class Benefit(Base):
    __tablename__ = "benefits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    tariffs: Mapped[list["TariffBenefit"]] = relationship(
        back_populates="benefit"
    )


class TariffBenefit(Base):
    __tablename__ = "tariff_benefits"

    id: Mapped[int] = mapped_column(primary_key=True)
    tariff_id: Mapped[int] = mapped_column(sa.ForeignKey("tariffs.id"))
    benefit_id: Mapped[int] = mapped_column(sa.ForeignKey("benefits.id"))

    tariff: Mapped["Tariff"] = relationship(back_populates="benefits")
    benefit: Mapped["Benefit"] = relationship(back_populates="tariffs")
