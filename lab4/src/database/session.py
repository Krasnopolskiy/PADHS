from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.database import DatabaseSettings


class DatabaseSessionManager:
    def __init__(self):
        engine = create_engine(url=DatabaseSettings().url)
        DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = DatabaseSession()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


async def get_db_session():
    with DatabaseSessionManager() as session:
        yield session
