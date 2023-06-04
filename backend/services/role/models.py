import sqlalchemy as sa

from services import Base
from services.role.schemas import RolesChoice


class Role(Base):
    __tablename__ = "roles"

    name = sa.Column(sa.Enum(RolesChoice), primary_key=True)
    permissions = sa.Column(sa.JSON)
