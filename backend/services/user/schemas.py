from typing import Optional

from fastapi import Form, UploadFile
from pydantic import BaseModel, EmailStr, Field

from services.role.schemas import RoleResponse


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SuccessResponse(BaseModel):
    status: str


class UserRead(BaseModel):
    id: int
    firstname: str | None
    lastname: str | None
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
    email: EmailStr
    hashed_password: str = Field(
        ...,
        alias="password",
        min_length=8,
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]|.*[_]).",
    )


class UserPatch(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    hashed_password: Optional[str]
    avatar_url: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        firstname: Optional[str] = Form(
            "", min_length=2, regex="^[a-zA-Zа-яА-ЯёЁ]+$"
        ),
        lastname: Optional[str] = Form(
            "", min_length=2, regex="^[a-zA-Zа-яА-ЯёЁ]+$"
        ),
        hashed_password: Optional[str] = Form(
            "",
            min_length=8,
            regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]|.*[_]).",
            alias="password",
        ),
        avatar_url: Optional[UploadFile] = Form(None, alias="picture"),
    ):
        return cls(
            firstname=firstname,
            lastname=lastname,
            hashed_password=hashed_password,
            avatar_url=avatar_url,
        )
