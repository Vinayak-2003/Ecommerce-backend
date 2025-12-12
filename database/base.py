from config import get_settings
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine, 
    async_sessionmaker
)

from utilities.logger_middleware import get_logger
logger = get_logger(__name__)

Base = declarative_base()
settings = get_settings()

DATABASE_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
                settings.DATABASE_USER, 
                settings.DATABASE_PASSWORD, 
                settings.DATABASE_HOST, 
                settings.DATABASE_PORT, 
                settings.DATABASE_NAME
            )
engine = None
async_session_factory = None

async def init_db():
    global engine, async_session_factory
    try:
        engine = create_async_engine(
            url=DATABASE_URL,
            echo=False,
            pool_size=10,
            max_overflow=0
        )

        async_session_factory = async_sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False
        )
        logger.info(f"Database connection pool initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing connection pool: {e}")
        raise e

async def close_db():
    global engine
    if engine:
        try:
            await engine.dispose()
            engine = None
            logger.info(f"Database connection pool closed successfully.")
        except Exception as e:
            logger.error(f"Error closing connection pool: {e}")
            raise e 

async def get_db_session():
    session: AsyncSession = async_session_factory()
    try:
        logger.info(f"Database connection acquired")
        yield session
        await session.commit()
    except Exception as e:
        logger.error(f"Error acqiring database connection: {e}")
        await session.rollback()
        raise e
    finally:
        logger.info(f"Database connection released back to pool")
        await session.close()
