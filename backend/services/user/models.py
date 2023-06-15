from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable

from services import Base
from services.role.models import Role
from services.role.schemas import RoleNameChoice
from settings import config


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    email: Mapped[str] = mapped_column(
        sa.String(length=320), unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(sa.String(length=1024))
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
    role = relationship(Role, backref="users", lazy="selectin")
