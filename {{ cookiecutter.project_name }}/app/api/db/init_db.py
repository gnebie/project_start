# init_db
import logging
from app.api.db.create_db_values import create_db_values
from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# Configure logger
logger = logging.getLogger(__name__)

sync_engine = None


def get_sync_engine(renew=False):
    """
    Get the synchronous database engine.

    :return: Synchronous SQLAlchemy engine
    """
    global sync_engine
    if not sync_engine or renew:
        logger.trace("Creating synchronous database engine")
        sync_engine = create_engine(settings.DB_URL)
    return sync_engine


def init_db():
    """
    Initialize the database in synchronous mode.

    This function creates all tables defined in the SQLModel metadata.
    """
    logger.trace("Initializing database in synchronous mode")
    engine = get_sync_engine()
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    """
    Get a synchronous database session.

    This function provides a session for interacting with the database in synchronous mode.

    :yield: Synchronous SQLAlchemy session
    """
    logger.trace("Creating synchronous database session")
    engine = get_sync_engine()
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        yield session
