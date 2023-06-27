from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services import Base


class ChatMember(Base):
    __tablename__ = "chat_members"

    tguser_id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    chats: Mapped[List["ChatsInMember"]] = relationship(
       back_populates="member", lazy="joined"
    )


class ParseredChat(Base):
    __tablename__ = "parsered_chats"

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        unique=True, index=True
    )
    description: Mapped[str] = mapped_column(nullable=True)
    members: Mapped[List["ChatsInMember"]] = relationship(
       back_populates="chat", lazy="joined"
    )


class ChatsInMember(Base):
    __tablename__ = "chats_in_members"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_member_name: Mapped[str] = mapped_column(
        sa.ForeignKey("chat_members.username")
    )
    parsered_chat_name: Mapped[str] = mapped_column(
        sa.ForeignKey("parsered_chats.name")
    )
    member: Mapped["ChatMember"] = relationship(
        back_populates="chats", lazy="joined"
    )
    chat: Mapped["ParseredChat"] = relationship(
        back_populates="members", lazy="joined"
    )
