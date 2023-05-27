from datetime import datetime

import sqlalchemy as sa
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    firstname = sa.Column(sa.String, nullable=False)
    lastname = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, default=datetime.utcnow())
    email = sa.Column(
        sa.String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password = sa.Column(sa.String(length=1024), nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    is_verified = sa.Column(sa.Boolean, default=False, nullable=False)
