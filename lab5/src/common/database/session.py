from opentelemetry import trace
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from common.config.database import DatabaseSettings
from common.utils.tracing import observed

tracer = trace.get_tracer(__name__)


class DatabaseSessionManager:
    def __init__(self):
        engine = create_engine(url=DatabaseSettings().url)
        DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = DatabaseSession()

    @observed(tracer)
    def __enter__(self) -> Session:
        return self.session

    @observed(tracer)
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
