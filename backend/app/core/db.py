from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.db_model import PostgresBase

engine = create_async_engine(
    settings.database.url,
    echo=settings.app.debug,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """Get a database session with automatic transaction management."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db() -> AsyncGenerator[AsyncSession]:
    """FastAPI dependency for database sessions."""
    async with get_db_session() as session:
        yield session


async def connect_database() -> None:
    logger.info("Connecting to PostgreSQL database...")

    try:
        async with engine.begin() as conn:
            await conn.run_sync(PostgresBase.metadata.create_all)

        logger.info("Database connected successfully!")

    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


async def close_database_connection() -> None:
    logger.info("Closing database connection...")
    await engine.dispose()
    logger.info("Database connection closed!")
