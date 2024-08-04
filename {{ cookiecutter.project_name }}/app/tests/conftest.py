# conftest.py

from http.client import HTTPException
from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

import logging
from app.config.settings import settings
from app.tests.test_config import DATABASE_URL

settings.DB_URL = DATABASE_URL
settings.LOG_LEVEL = "TRACE"

from app.create_app import app
from app.api.db import async_init_db, get_async_session, get_async_engine
from app.api.models.billing import *

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="session")
def engine():
    return create_async_engine(DATABASE_URL, echo=True)


@pytest.fixture(scope="session")
async def setup_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def session(engine, setup_database) -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

