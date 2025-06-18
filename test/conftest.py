import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.db.base import Base
from app.main import app
from httpx import AsyncClient, ASGITransport


TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/test_task_db"

# Engine для миграций и подготовки БД (например, для run_sync)
prepare_engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Асинхронный engine для тестов и клиента
engine_test = create_async_engine(TEST_DATABASE_URL, echo=True)

async_session_test = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture(scope="function")
async def connection():
    async with engine_test.connect() as conn:
        trans = await conn.begin()
        yield conn
        await trans.rollback()


@pytest_asyncio.fixture(scope="function")
async def db_session(connection):
    async_session = async_sessionmaker(bind=connection, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        session.rollback()

@pytest_asyncio.fixture(scope="function")
async def prepare_database():
    # Создаем таблицы в тестовой БД
    async with engine_test.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # очистка перед тестами
        await conn.run_sync(Base.metadata.create_all)  # создание таблиц
        await conn.commit()
#
    yield

    # После всех тестов можно очистить БД
    async with engine_test.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


@pytest_asyncio.fixture
async def db_session(prepare_database):
    async with async_session_test() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def async_client():
    # Подменяем в приложении зависимость сессии на тестовую
    from app.db.base import get_async_session  # предполагается, что у тебя есть get_db зависимость

    async def override_get_db():
        async with async_session_test() as session:
            yield session

    app.dependency_overrides.clear()
    app.dependency_overrides[get_async_session] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()
