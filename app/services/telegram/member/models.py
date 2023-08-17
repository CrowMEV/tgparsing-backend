from typing import List

import sqlalchemy as sa
from services import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


chat_member = sa.Table(
    "chat_member",
    Base.metadata,
    sa.Column("chat_id", sa.ForeignKey("chats.id"), primary_key=True),
    sa.Column("member_id", sa.ForeignKey("members.id"), primary_key=True),
)


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True)
    chat_id: Mapped[int] = mapped_column(sa.BIGINT)
    title: Mapped[str] = mapped_column(unique=True, index=True, default="")
    description: Mapped[str] = mapped_column(nullable=True, default="")
    username: Mapped[str] = mapped_column(index=True)
    members: Mapped[List["Member"]] = relationship(
        secondary=chat_member,
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
        secondary=chat_member,
        back_populates="members",
        lazy="joined",
    )
