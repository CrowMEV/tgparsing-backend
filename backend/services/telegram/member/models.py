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
    title: Mapped[str] = mapped_column(unique=True, index=True, default="")
    description: Mapped[str] = mapped_column(nullable=True, default="")
    username: Mapped[str] = mapped_column(index=True)
    members: Mapped[List["Member"]] = relationship(
        secondary=chats_members,
        back_populates="chats",
        lazy="joined",
    )


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.BIGINT)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=True
    )
    phone_number: Mapped[str] = mapped_column(nullable=True)
    chats: Mapped[List["Chat"]] = relationship(
        secondary=chats_members,
        back_populates="members",
        lazy="joined",
    )
