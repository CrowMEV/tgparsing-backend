import decimal
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services import Base
from services.payment.models import Payment
from services.role.models import Role
from services.role.schemas import RoleNameChoice
from services.tariff.models import UserSubscribe
from settings import config


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    email: Mapped[str] = mapped_column(
        sa.String(length=320), unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(sa.String(length=1024))
    phone_number: Mapped[str] = mapped_column(nullable=True, unique=True)
    timezone: Mapped[int] = mapped_column(
        sa.SMALLINT,
        default=0,
        server_default="0",
    )
    avatar_url: Mapped[str] = mapped_column(
        default=config.base_avatar_url,
        server_default=config.base_avatar_url,
    )
    is_active: Mapped[bool] = mapped_column(
        default=config.IS_ACTIVE,
        server_default=sa.text(f"{config.IS_ACTIVE}"),
    )
    is_staff: Mapped[bool] = mapped_column(
        default=False, server_default=sa.false()
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False, server_default=sa.false()
    )
    is_verified: Mapped[bool] = mapped_column(
        default=False, server_default=sa.false()
    )
    role_name: Mapped[RoleNameChoice] = mapped_column(
        sa.ForeignKey("roles.name"),
        default=RoleNameChoice.USER,
        server_default=RoleNameChoice.USER.name,
    )
    subscribe: Mapped[UserSubscribe] = relationship(
        backref="user", uselist=False, lazy="joined"
    )
    role = relationship(Role, backref="users", lazy="joined")
    balance: Mapped[decimal.Decimal] = mapped_column(
        default=0,
        onupdate=sa.select(
            sa.func.sum(Payment.amount)  # pylint: disable=E1102
        ).where(Payment.status == sa.true()),
    )
