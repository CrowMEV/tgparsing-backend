from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services import Base

chats_members = sa.Table(
    "chats_members",
    Base.metadata,
    sa.Column("chat", sa.ForeignKey("chats.id"), primary_key=True),
    sa.Column("member", sa.ForeignKey("members.id"), primary_key=True),
)


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    members: Mapped[List["Member"]] = relationship(
        secondary=chats_members,
        back_populates="chats",
    )


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    chats: Mapped[List["Chat"]] = relationship(
        secondary=chats_members,
        back_populates="members",
    )
