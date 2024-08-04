# async_init_db
import logging
from typing import AsyncGenerator
from app.api.db.create_db_values import create_db_values
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine

# Configure logger
logger = logging.getLogger(__name__)

async_engine = None


def get_async_engine(renew=False):
    """
    Get the asynchronous database engine.

    :return: Asynchronous SQLAlchemy engine
    """
    global async_engine
    if not async_engine or renew:
        logger.trace(f"Creating asynchronous database engine : {settings.DB_URL}")
        async_engine = create_async_engine(settings.DB_URL, echo=True)
    return async_engine


async def async_init_db():
    """
    Initialize the database in asynchronous mode.

    This function creates all tables defined in the SQLModel metadata.
    """
    logger.trace("Initializing database in asynchronous mode")
    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create the base values like the roles
    if settings.DB_CREATE_BASE_VALUES:
        await create_db_values(engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an asynchronous database session.

    This function provides a session for interacting with the database in asynchronous mode.

    :yield: Asynchronous SQLAlchemy session
    """
    logger.trace("Creating asynchronous database session")
    async_engine = get_async_engine()
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
