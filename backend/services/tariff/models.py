import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from services import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
