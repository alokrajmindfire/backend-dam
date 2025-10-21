from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class DatabaseSettings(BaseSettings):
    """
    Pydantic settings model for database connection.
    """
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: Optional[str] = None # Can be used for a full connection string

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Instantiate your settings
db_settings = DatabaseSettings()