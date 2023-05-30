from typing import Optional

from fastapi import Query
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, BaseModel, Field
from fastapi_users import schemas


class Permissions(BaseModel):
    read: bool = False
    write: bool = False


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=1, regex='^[a-zA-Z]+$')
    permissions: Permissions = Permissions()


class RoleUpdate(BaseModel):
    name: str = Field(..., min_length=1, regex='^[a-zA-Z]+$')
    permissions: Permissions = Permissions(read=True, write=False)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLogout(BaseModel):
    status: str


class UserRead(schemas.BaseUser):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    role_id: int

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    firstname: str = Field(..., min_length=1, regex='^[a-zA-Z]+$')
    lastname: str = Field(..., min_length=1, regex='^[a-zA-Z]+$')
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        regex=r'([0-9]+\S*[A-Z]+|[A-Z]+\S*[0-9]+)\S*'
              '[!"`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+'
    )
    role_id: int = 1


class UserUpdate(schemas.BaseUserUpdate):
    pass
