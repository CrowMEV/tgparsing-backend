import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    api_id = sa.Column(sa.Integer, nullable=False, unique=True)
    api_hash = sa.Column(sa.String, nullable=False)
    session = sa.Column(sa.String, nullable=False)
    is_blocked = sa.Column(sa.Boolean, default=False)
    is_worked = sa.Column(sa.Boolean, default=False)
    by_geo = sa.Column(sa.Boolean, default=False)
