from pydantic import BaseModel


class TgAccountRead(BaseModel):
    # id: int
    # api_id: int
    # api_hash: str
    # session_strins: str
    # in_work: bool
    # is_blocked: bool
    # by_geo: bool

    class Config:
        orm_mode = True


class TgAccountCreate(BaseModel):
    api_id: int
    api_hash: str
    session_string: str


class TgAccountResponse(TgAccountCreate):
    # Inherit fields from RolePatch

    class Config:
        orm_mode = True


class TgAccountUpdate(BaseModel):
    session_string: str
    in_work: bool
    is_blocked: bool
    by_geo: bool
