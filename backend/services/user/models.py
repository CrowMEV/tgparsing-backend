from datetime import datetime

import sqlalchemy as sa
from fastapi_users.db import SQLAlchemyBaseUserTable

from services import Base
from services.role.models import Role
from services.role.schemas import RolesChoice
from settings import config
from sqlalchemy.orm import relationship


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    firstname = sa.Column(sa.String, nullable=False)
    lastname = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, default=datetime.utcnow())
    email = sa.Column(
        sa.String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password = sa.Column(sa.String(length=1024), nullable=False)
    avatar_url = sa.Column(sa.String, default=config.base_avatar_url)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_staff = sa.Column(sa.Boolean, nullable=False, default=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    is_verified = sa.Column(sa.Boolean, default=False, nullable=False)
    role_name = sa.Column(
        sa.Enum(RolesChoice),
        sa.ForeignKey("roles.name", name="users_roles_name_fkey"),
        default=RolesChoice.user,
        nullable=False,
    )
    role = relationship(
        Role,
        backref="users",
        lazy="selectin",
    )
