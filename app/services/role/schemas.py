import enum
from typing import Optional

from pydantic import BaseModel, Field


class RoleNameChoice(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    HR = "hr"
    SUPERUSER = "superuser"


class RoleGet(BaseModel):
    name: RoleNameChoice


class RoleResponse(RoleGet):
    # Inherit name from RoleGet
    is_active: bool

    class Config:
        orm_mode = True


class RolePatch(RoleGet):
    # Inherit name from RoreGet
    is_active: Optional[bool]


class Permissions(BaseModel):
    read: bool = False
    write: bool = False


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=1, regex="^[a-zA-Z]+$")
    permissions: Permissions = Permissions()


class RoleUpdate(BaseModel):
    name: str = Field(..., min_length=1, regex="^[a-zA-Z]+$")
    permissions: Permissions = Permissions(read=True, write=False)
