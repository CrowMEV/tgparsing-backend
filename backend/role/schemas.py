from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import BaseModel


class Permissions(BaseModel):
    read: bool
    write: bool


class RoleCreate(BaseModel):
    name: str
    permissions: Permissions


class RoleUpdate(BaseModel):
    name: str
    permissions: Permissions

