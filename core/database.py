from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.settings import settings


engine = create_engine(
    settings.DATABASE_DSN,
    echo=True if settings.ENVIRONMENT == "development" else False
)


def get_session():
    return Session(engine)
