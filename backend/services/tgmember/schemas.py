from typing import Optional
from pydantic import BaseModel


class ChatMember(BaseModel):
    tguser_id: int
    username: str
    chat_names: list[str]


class ParseredChat(BaseModel):
    chat_id: int
    name: str


class ChatMemberRead(ChatMember):
    firstname: str
    lastname: str

    class Config:
        orm_mode = True


class ParseredChatRead(ParseredChat):
    title: str

    class Config:
        orm_mode = True


class ChatMemberCreate(ChatMember):
    firstname: Optional[str]
    lastname: Optional[str]

    class Config:
        orm_mode = True


class ParseredChatCreate(ParseredChat):
    title: Optional[str]

    class Config:
        orm_mode = True
