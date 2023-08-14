import decimal
from datetime import datetime

import sqlalchemy as sa
from database.utils import UtcNow
from services import Base
from services.role.models import Role
from services.role.schemas import RoleNameChoice
from services.tariff.models import UserSubscribe
from settings import config
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(server_default="", default="")
    lastname: Mapped[str] = mapped_column(server_default="", default="")
    created_at: Mapped[datetime] = mapped_column(server_default=UtcNow())
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
        default=str(config.base_avatar_url),
        server_default=str(config.base_avatar_url),
    )
    is_banned: Mapped[bool] = mapped_column(
        default=False,
        server_default=sa.false(),
    )
    is_staff: Mapped[bool] = mapped_column(
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
    balance: Mapped[decimal.Decimal] = mapped_column(
        default=0, server_default="0"
    )
    role = relationship(Role, backref="users", lazy="joined")
    subscribe = relationship(
        UserSubscribe, backref="user", lazy="joined", uselist=False
    )
