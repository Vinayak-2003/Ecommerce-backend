from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str = "127.0.0.1"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str

    ALLOWED_ORIGINS: list[str]

    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_TIME: int = 30
    REFRESH_TOKEN_EXPIRE_TIME: int = 2 * 24 * 60
    ALGORITHM: str = "HS256"

    SUPABASE_PROJECT_URL: str
    SUPABASE_API_KEY: str
    SUPABASE_USER_ID: str
    SUPABASE_HOST: str
    SUPABASE_DB_PASSWORD: str
    SUPABASE_DATABASE_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()
