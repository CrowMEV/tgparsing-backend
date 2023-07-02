import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

import services.telegram.account.schemas as tg_schemas
from services import Base


class TgAccount(Base):
    __tablename__ = "tgacounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    api_id: Mapped[int] = mapped_column(unique=True)
    api_hash: Mapped[str] = mapped_column(sa.String(length=400))
    session_string: Mapped[str]
    work_status: Mapped[tg_schemas.WorkChoice] = mapped_column(
        default=tg_schemas.WorkChoice.FREE
    )
    block_status: Mapped[tg_schemas.BlockChoice] = mapped_column(
        default=tg_schemas.BlockChoice.UNBLOCK
    )
