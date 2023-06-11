import enum

from pydantic import BaseModel


class WorkChoice(enum.Enum):
    WORK = 'work'
    FREE = 'free'
    EMPTY = ''


class BlockChoice(enum.Enum):
    BLOCK = 'block'
    UN_BLOCK = 'un_block'
    EMPTY = ''


class GeoChoice(enum.Enum):
    BY_GEO = 'by_geo'
    NOT_GEO = 'not_geo'
    EMPTY = ''


class TgAccountRead(BaseModel):
    id: int
    api_id: int
    api_hash: str
    session_string: str
    work: WorkChoice = WorkChoice.EMPTY
    blocked: BlockChoice = BlockChoice.EMPTY
    by_geo: GeoChoice = GeoChoice.EMPTY

    class Config:
        orm_mode = True


class TgAccountResponse(TgAccountRead):

    class Config:
        orm_mode = True
