import decimal
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import Form, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from services.role.schemas import RoleNameChoice, RoleResponse
from services.tariff.schemas import UserSubscribeResponse
from typing_extensions import Annotated
from utils.validators import Regex


NAME_PATTER = r"^[А-ЯA-ZЁ][а-яa-zё]*(-[А-ЯA-ZЁ][а-яa-zё]*)?$"
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]|.*[_])."


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
    is_banned: bool
    is_verified: bool = False
    avatar_url: str
    role: RoleResponse
    phone_number: str | None
    created_at: datetime
    balance: decimal.Decimal
    subscribe: UserSubscribeResponse | None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: Annotated[str, Regex(PASSWORD_PATTERN)] = Field(
        ..., min_length=8, alias="password"
    )
    timezone: Optional[int] = Field(default=0, ge=-12, le=12)


@dataclass
class UserPatch:
    firstname: str = Form(
        default=None,
        min_length=1,
        max_length=61,
        pattern=NAME_PATTER,
    )
    lastname: str = Form(
        default=None,
        min_length=1,
        max_length=61,
        pattern=NAME_PATTER,
    )
    timezone: int = Form(default=None, ge=-12, le=12)
    hashed_password: str = Form(
        default=None,
        min_length=8,
        alias="password",
    )
    avatar_url: UploadFile = Form(default=None, alias="picture")
    email: EmailStr = Form(default=None)
    phone_number: str = Form(
        default=None,
        min_length=8,
        pattern=r"^\+[0-9+][0-9()-]{4,14}\d$",
    )

    def __post_init__(self):
        if self.avatar_url and not self.avatar_url.content_type:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Picture can't be empty",
            )
        if self.hashed_password:
            checked_password = re.match(PASSWORD_PATTERN, self.hashed_password)
            if not checked_password:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Picture can't be empty",
                )


@dataclass
class UserPatchByAdmin(UserPatch):
    role_name: RoleNameChoice = Form(default=None, alias="role")
