import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from services.role.schemas import RolesChoice


Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    name = sa.Column(sa.Enum(RolesChoice), primary_key=True)
    permissions = sa.Column(sa.JSON)
