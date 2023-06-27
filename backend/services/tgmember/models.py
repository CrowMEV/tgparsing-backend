import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services import Base


class ChatMember(Base):
    __tablename__ = "chat_members"
    __table_args__ = (
        sa.UniqueConstraint("username", name="tgusername_unique"),
    )
    tguser_id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str]
    chat_names: Mapped[list["ParseredChat"]] = mapped_column(
        sa.ForeignKey("parsered_chats.name")
    )
    chats: Mapped[list["ParseredChat"]] = relationship(
        back_populates="chat_member"
    )


class ParseredChat(Base):
    __tablename__ = "parsered_chats"
    __table_args__ = (
        sa.UniqueConstraint("name", name="chatname_unique"),
    )
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    title: Mapped[str] = mapped_column(nullable=True)
    chat_member: Mapped[ChatMember] = relationship(back_populates="chats")
