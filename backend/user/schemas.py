from typing import Optional, TypeVar

from fastapi import UploadFile
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, BaseModel, Field
from fastapi_users import schemas


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SuccessResponse(BaseModel):
    status: str


class UserRead(schemas.BaseUser):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    avatar_url: str

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    firstname: str = Field(..., min_length=1, regex='^[a-zA-Zа-яА-яёЁ]+$')
    lastname: str = Field(..., min_length=1, regex='^[a-zA-Zа-яА-яёЁ]+$')
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        regex=r'([0-9]+\S*[A-Z]+|\S[A-Z]+\S*[0-9]+)\S*'
              r'[!\"`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+'
    )


class UserPatch(CreateUpdateDictModel):
    firstname: Optional[str] = Field('')
    lastname: Optional[str] = Field('')
    password: Optional[str] = Field('')
    avatar_url: Optional[str] = Field('')


class UserUpdate(schemas.BaseUserUpdate):
    pass


UP = TypeVar("UP", bound=UserPatch)
