from sqlalchemy import create_engine, text
from config import get_settings
from sqlalchemy.orm import sessionmaker

settings = get_settings()

def get_ecommercebackend_db_conn():
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
        print(f"Database connected successfully !!")
        return engine
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise


def get_db_session():
    db = sessionmaker(bind=get_ecommercebackend_db_conn())
    try:
        yield db
    finally:
        db.close()