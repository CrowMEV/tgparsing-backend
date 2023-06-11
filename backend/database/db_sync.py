from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import config


engine = create_engine(config.sync_url, echo=config.DB_ECHO)
Session = sessionmaker(bind=engine)


def db_sync():
    with Session() as session:
        yield session


def create_db_session():
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
