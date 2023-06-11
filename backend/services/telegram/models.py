from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from services import Base
import services.telegram.schemas as tg_schemas


class TgAccount(Base):
    __tablename__ = 'tgacounts'

    id: Mapped[int] = mapped_column(primary_key=True)
    api_id: Mapped[int]
    api_hash: Mapped[str]
    session_string: Mapped[str]
    work: Mapped[tg_schemas.WorkChoice] = mapped_column(
        default=tg_schemas.WorkChoice.FREE
    )
    blocked: Mapped[tg_schemas.BlockChoice] = mapped_column(
        default=tg_schemas.BlockChoice.UN_BLOCK
    )
    by_geo: Mapped[tg_schemas.GeoChoice] = mapped_column(
        default=tg_schemas.GeoChoice.BY_GEO
    )
