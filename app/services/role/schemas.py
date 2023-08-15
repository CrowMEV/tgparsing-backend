import enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoleNameChoice(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    HR = "hr"
    SUPERUSER = "superuser"


class RoleGet(BaseModel):
    name: RoleNameChoice
    pretty_name: str


class RoleResponse(RoleGet):
    # Inherit name from RoleGet
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RolePatch(RoleGet):
    # Inherit name from RoreGet
    is_active: Optional[bool]
