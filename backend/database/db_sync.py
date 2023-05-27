from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import config


engine = create_engine(config.sync_url, echo=True)
Session = sessionmaker(bind=engine)


def db_sync():
    with Session() as session:
        yield session
