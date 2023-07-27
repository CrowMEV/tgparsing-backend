from settings import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(config.sync_url, echo=config.DB_ECHO)
Session = sessionmaker(bind=engine)


def db_sync():
    with Session() as session:
        yield session
