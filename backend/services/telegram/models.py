from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from services import Base


class TgAccount(Base):
    __tablename__ = 'tgacounts'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    api_id: int = sa.Column(sa.Integer, nullable=False)
    api_hash: str = sa.Column(sa.String, nullable=False)
    session_string: str = sa.Column(sa.String, nullable=False)
    in_work: bool = sa.Column(sa.Boolean, default=False)
    is_blocked: bool = sa.Column(sa.Boolean, default=False)
    by_geo: bool = sa.Column(sa.Boolean, default=False)
