import sqlalchemy as sa

from services import Base
from services.role.schemas import RolesChoice


class Role(Base):
    __tablename__ = "roles"

    name: str = sa.Column(sa.Enum(RolesChoice), primary_key=True)
    is_active: bool = sa.Column(sa.Boolean, default=True)
    permissions: dict = sa.Column(sa.JSON)
