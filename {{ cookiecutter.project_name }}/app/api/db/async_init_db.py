# async_init_db
import logging
from typing import AsyncGenerator
from app.api.db.create_db_values import create_db_values
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine, text
import asyncpg

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
        echo_db_values = False
        async_engine = create_async_engine(settings.DB_URL, echo=echo_db_values)
    return async_engine


async def async_init_db():
    """
    Initialize the database in asynchronous mode.

    This function creates all tables defined in the SQLModel metadata.
    """
    logger.trace("Initializing database in asynchronous mode")
    if settings.DB_CREATE_BASE_VALUES:
        db_name = settings.DB_URL.split("/")[-1]
        db_root_url = settings.DB_URL[: -(len(db_name) + 1)]
        logger.trace(f"Create the database if not exiting url : {db_root_url}    database name : {db_name}")
        await create_database_if_not_exists(db_root_url, db_name)
    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

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


def prepare_db_url_for_asyncpg(db_url):
    return db_url.replace("postgresql+asyncpg://", "postgresql://")


async def create_database_if_not_exists(db_url: str, db_name: str):
    # Create a temporary engine to connect to the server without specifying the database
    logger.trace(f"Creating  database if not exist ")
    db_url_for_asyncpg = prepare_db_url_for_asyncpg(db_url)
    conn = await asyncpg.connect(db_url_for_asyncpg)
    try:
        # Check if the database exists
        result = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
        if not result:
            logger.trace(f"Creating {db_name} database ")
            # Create the database without a transaction
            await conn.execute(f"CREATE DATABASE {db_name}")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        await conn.close()
