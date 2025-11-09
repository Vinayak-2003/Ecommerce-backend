from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import get_settings
from sqlalchemy.orm import declarative_base
from utilities.logger_middleware import get_logger

logger = get_logger(__name__)


Base = declarative_base()
settings = get_settings()

def get_ecommercedatabase_db_conn():
    try:
        engine = create_engine(
            url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
                settings.DATABASE_USER, 
                settings.DATABASE_PASSWORD, 
                settings.DATABASE_HOST, 
                settings.DATABASE_PORT, 
                settings.DATABASE_NAME
            )
        )

        # test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connected successfully !!")
        return engine
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


def get_db_session():
    Session = sessionmaker(bind=get_ecommercedatabase_db_conn())
    session = Session()
    try:
        yield session
    finally:
        session.close()
