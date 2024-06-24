import logging
from app.api.db.create_db_values import create_db_values
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine

# Configure logger
logger = logging.getLogger(__name__)

def get_sync_engine():
    """
    Get the synchronous database engine.

    :return: Synchronous SQLAlchemy engine
    """
    logger.trace("Creating synchronous database engine")
    return create_engine(settings.DB_URL)

def get_async_engine():
    """
    Get the asynchronous database engine.

    :return: Asynchronous SQLAlchemy engine
    """
    logger.trace("Creating asynchronous database engine")
    return create_async_engine(settings.DB_URL, echo=True)

def init_db():
    """
    Initialize the database in synchronous mode.

    This function creates all tables defined in the SQLModel metadata.
    """
    logger.trace("Initializing database in synchronous mode")
    engine = get_sync_engine()
    SQLModel.metadata.create_all(bind=engine)

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

async def get_async_session() -> AsyncSession:
    """
    Get an asynchronous database session.

    This function provides a session for interacting with the database in asynchronous mode.

    :yield: Asynchronous SQLAlchemy session
    """
    logger.trace("Creating asynchronous database session")
    async_engine = get_async_engine()
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session