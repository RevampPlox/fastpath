from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from app.core.database import get_session
from app.main import app
from app.models.table_model import TableModel


@pytest_asyncio.fixture(scope='session')
def engine() -> Generator[AsyncEngine]:
    with PostgresContainer('postgres:17-alpine', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncConnection]:
    async with engine.begin() as conn:
        await conn.run_sync(TableModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(TableModel.metadata.drop_all)


@pytest.fixture
def client(session: AsyncSession) -> Generator[TestClient]:
    def get_session_overdrive() -> AsyncSession:
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_overdrive
        yield client
        app.dependency_overrides.clear()
