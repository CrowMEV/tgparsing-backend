import sqlalchemy as sa
from services import Base
from services.role.schemas import RoleNameChoice
from sqlalchemy.orm import Mapped, mapped_column


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[RoleNameChoice] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=sa.true()
    )
    pretty_name: Mapped[str]
