from typing import Optional

from fastapi import Form, UploadFile
from pydantic import EmailStr, BaseModel, Field

from services.role.schemas import RoleResponse


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SuccessResponse(BaseModel):
    status: str


class UserRead(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    is_staff: bool
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    avatar_url: str
    role: RoleResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    firstname: str = Field(..., min_length=1, regex="^[a-zA-Zа-яА-яёЁ]+$")
    lastname: str = Field(..., min_length=1, regex="^[a-zA-Zа-яА-яёЁ]+$")
    email: EmailStr
    hashed_password: str = Field(
        ...,
        alias="password",
        min_length=8,
        regex=r""
        r"((\d|\w)*[A-Z]+(\d|\w)*[0-9]+(\d|\w)*|"
        r"(\d|\w)*[0-9]+(\d|\w)*[A-Z]+(\d|\w)*)"
        r"[!\"`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+",
    )


class UserPatch(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    password: Optional[str]
    avatar_url: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        firstname: Optional[str] = Form(
            "", min_length=1, regex="^[a-zA-Zа-яА-яёЁ]+$"
        ),
        lastname: Optional[str] = Form(
            "", min_length=1, regex="^[a-zA-Zа-яА-яёЁ]+$"
        ),
        password: Optional[str] = Form(
            "",
            min_length=8,
            regex=r""
            r"((\d|\w)*[A-Z]+(\d|\w)*[0-9]+(\d|\w)*|"
            r"(\d|\w)*[0-9]+(\d|\w)*[A-Z]+(\d|\w)*)"
            r"[!\"`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+",
        ),
        avatar_url: Optional[UploadFile] = Form(None, alias="picture"),
    ):
        return cls(
            firstname=firstname,
            lastname=lastname,
            password=password,
            avatar_url=avatar_url,
        )
