from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, ForeignKey, TIMESTAMP


metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('firstname', String, nullable=False),
    Column('lastname', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('registred_at', TIMESTAMP, default=datetime.utcnow),
    Column('email', String(length=320), unique=True, index=True, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)
