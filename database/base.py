"""
Core database configuration and session management for the E-Commerce Backend.
"""
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from config import get_settings
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)

Base = declarative_base()
settings = get_settings()

DATABASE_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
    settings.SUPABASE_USER_ID,
    settings.SUPABASE_DB_PASSWORD,
    settings.SUPABASE_HOST,
    settings.DATABASE_PORT,
    settings.SUPABASE_DATABASE_NAME,
)

engine = None
async_session_factory = None


async def init_db():
    """
    Initializes the database engine and session factory.
    """
    global engine, async_session_factory
    try:
        engine = create_async_engine(
            url=DATABASE_URL, echo=False, pool_size=10, max_overflow=0
        )

        async_session_factory = async_sessionmaker(
            bind=engine, autocommit=False, autoflush=False
        )
        logger.info("Database connection pool initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing connection pool: {e}")
        raise e


async def close_db():
    """
    Disposes of the database engine and closes all connections in the pool.
    """
    global engine
    if engine:
        try:
            await engine.dispose()
            engine = None
            logger.info("Database connection pool closed successfully.")
        except Exception as e:
            logger.error(f"Error closing connection pool: {e}")
            raise e


async def get_db_session():
    """
    Dependency that provides an async database session and handles transaction commits/rollbacks.
    """
    session: AsyncSession = async_session_factory()
    try:
        logger.info("Database connection acquired")
        yield session
        await session.commit()
    except Exception as e:
        logger.error(f"Error acqiring database connection: {e}")
        await session.rollback()
        raise e
    finally:
        logger.info("Database connection released back to pool")
        await session.close()
