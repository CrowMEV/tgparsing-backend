from typing import Optional

from pydantic import BaseModel


class TgAccountRead(BaseModel):
    id: int
    api_id: int
    api_hash: str
    session_string: str
    in_work: bool
    is_blocked: bool
    by_geo: bool


class TgAccountCreate(BaseModel):
    api_id: int
    api_hash: str
    session_string: str


class TgAccountResponse(TgAccountRead):
    # Inherit fields from RolePatch

    class Config:
        orm_mode = True


class TgAccountUpdate(BaseModel):
    session_string: str
    in_work: bool
    is_blocked: bool
    by_geo: bool
