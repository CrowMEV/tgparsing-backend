import decimal
from datetime import datetime
from typing import Optional

from fastapi import Form, UploadFile
from pydantic import BaseModel, EmailStr, Field, root_validator
from services.role.schemas import RoleResponse
from services.tariff.schemas import UserSubscribeResponse


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
    timezone: int
    is_staff: bool
    is_active: bool = True
    is_verified: bool = False
    avatar_url: str
    role: RoleResponse
    phone_number: str | None
    created_at: datetime
    balance: decimal.Decimal
    subscribe: UserSubscribeResponse | None

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
    timezone: Optional[int] = Field(default=0, ge=-12, le=12)


class UserPatch(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    timezone: Optional[int]
    hashed_password: Optional[str]
    avatar_url: Optional[UploadFile]
    email: Optional[EmailStr]
    phone_number: Optional[str]

    @classmethod
    def as_form(
        cls,
        firstname: Optional[str] = Form(
            default=None, min_length=2, regex="^[a-zA-Zа-яА-ЯёЁ]+$"
        ),
        lastname: Optional[str] = Form(
            default=None, min_length=2, regex="^[a-zA-Zа-яА-ЯёЁ]+$"
        ),
        timezone: Optional[int] = Form(default=None, ge=-12, le=12),
        hashed_password: Optional[str] = Form(
            default=None,
            min_length=8,
            regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]|.*[_]).",
            alias="password",
        ),
        avatar_url: Optional[UploadFile] = Form(default=None, alias="picture"),
        email: Optional[EmailStr] = Form(default=None),
        phone_number: Optional[str] = Form(
            default=None,
            min_length=8,
            regex=r"^\+[0-9+][0-9()-]{4,14}\d$",
        ),
    ):
        return cls(
            firstname=firstname,
            lastname=lastname,
            timezone=timezone,
            hashed_password=hashed_password,
            avatar_url=avatar_url,
            email=email,
            phone_number=phone_number,
        )

    @root_validator
    def check_data_exists(cls, values):  # pylint: disable=E0213
        new_values = {
            key: value for key, value in values.items() if value is not None
        }
        return new_values
