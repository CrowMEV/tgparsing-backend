import enum
from typing import Optional, List

from pydantic import BaseModel, Field


class RoleNameChoice(enum.Enum):
    USER = "user"
    ADMIN = "admin"
    ACCOUNTANT = "accountant"
    HR = "hr"


class ActionChoice(enum.Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    UPDATE = "update"


class RoleGet(BaseModel):
    name: RoleNameChoice


class RolePatch(RoleGet):
    # Inherit name from RoreGet
    is_active: Optional[bool]
    staff_action: Optional[List[ActionChoice]]
    payment_action: Optional[List[ActionChoice]]
    role_action: Optional[List[ActionChoice]]


class RoleResponse(RolePatch):
    # Inherit fields from RolePatch

    class Config:
        orm_mode = True


class Permissions(BaseModel):
    read: bool = False
    write: bool = False


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=1, regex="^[a-zA-Z]+$")
    permissions: Permissions = Permissions()


class RoleUpdate(BaseModel):
    name: str = Field(..., min_length=1, regex="^[a-zA-Z]+$")
    permissions: Permissions = Permissions(read=True, write=False)
