from datetime import datetime, time

import sqlalchemy as sa
from services import Base
from services.telegram.tasks import schemas
from services.user.models import User
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=True,
        default=datetime.utcnow(),
    )
    job_start: Mapped[datetime] = mapped_column(
        nullable=True,
        default=datetime.utcnow(),
    )
    job_finish: Mapped[datetime] = mapped_column(
        nullable=True,
    )
    title: Mapped[str] = mapped_column(index=True)
    operation: Mapped[schemas.OperationChoice] = mapped_column(
        default=schemas.OperationChoice.PARSING,
        server_default=schemas.OperationChoice.PARSING.name,
    )
    work_status: Mapped[schemas.WorkStatusChoice] = mapped_column(
        default=schemas.WorkStatusChoice.IN_PROCESSING,
        server_default=schemas.WorkStatusChoice.IN_PROCESSING.name,
    )
    data_count: Mapped[int] = mapped_column(default=0)
    time_work: Mapped[datetime] = mapped_column(sa.TIME, default=time(0, 0, 0))
    favorite: Mapped[bool] = mapped_column(nullable=True, default=sa.false())
    user_id: Mapped[int] = mapped_column(sa.ForeignKey(User.id))
    user: Mapped[User] = relationship(
        backref="tasks",
        lazy="joined",
    )
    file_url: Mapped[str] = mapped_column(default="")
