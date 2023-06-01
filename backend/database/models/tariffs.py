import sqlalchemy as sa
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Tariff(Base):
    __tablename__ = "tariffs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
