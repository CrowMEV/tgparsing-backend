import enum
from typing import Optional

from pydantic import BaseModel


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

    class Config:
        orm_mode = True


class RolePatch(RoleGet):
    # Inherit name from RoreGet
    is_active: Optional[bool]
