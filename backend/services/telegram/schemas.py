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
    session_strins: str


class TgAccountUpdate(BaseModel):
    session_strins: str
    in_work: bool
    is_blocked: bool
    by_geo: bool
