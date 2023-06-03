from typing import Optional

from pydantic import BaseModel, Field


class AccountRead(BaseModel):
    api_id: int
    api_hash: str
    session: str
    is_blocked: bool
    is_worked: bool
    by_geo: bool


class AccountUpdate(BaseModel):
    api_id: Optional[int]
    api_hash: Optional[str]
    session: Optional[str]
    is_blocked: Optional[bool]
    is_worked: Optional[bool]
    by_geo: Optional[bool]


class AccountCreate(BaseModel):
    api_id: int
    api_hash: str
    session: str
    by_geo: bool
