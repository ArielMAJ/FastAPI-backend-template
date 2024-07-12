"""
Application's and its environment's configuration.
"""

import os


class DatabaseConfig:
    """Database configuration."""

    DATABASE_CONNECTOR = os.getenv("DATABASE_CONNECTOR", "postgresql+asyncpg")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "postgres")
    POSTGRES_URI = (
        f"{DATABASE_CONNECTOR}:"
        f"//{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    )
    POSTGRES_ECHO = os.getenv("POSTGRES_ECHO", "false").lower() == "true"


class Config:
    """Base configuration."""

    ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
    DEBUG = ENVIRONMENT == "DEV"
    TESTING = ENVIRONMENT == "TEST"

    HOST = os.getenv("APPLICATION_HOST", "127.0.0.1")
    PORT = int(os.getenv("APPLICATION_PORT", "3000"))
    WORKERS_COUNT = int(os.getenv("WORKERS_COUNT", "1"))
    RELOAD = os.getenv("RELOAD", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    APPLICATION_ROOT = os.getenv("APPLICATION_ROOT", "")

    DATABASE: DatabaseConfig = DatabaseConfig()


class TestConfig(Config):
    """Test configuration."""

    ENVIRONMENT = "test"
    TESTING = True
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
