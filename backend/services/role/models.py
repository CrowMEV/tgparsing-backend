from typing import List

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from services import Base
from services.role.schemas import RoleNameChoice, ActionChoice


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[RoleNameChoice] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=sa.true()
    )
    staff_action: Mapped[List[ActionChoice]] = mapped_column(
        ARRAY(sa.Enum(ActionChoice)),
        default=[],
        server_default="{}",
    )
    payment_action: Mapped[List[ActionChoice]] = mapped_column(
        ARRAY(sa.Enum(ActionChoice)),
        default=[],
        server_default="{}",
    )
