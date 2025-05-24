"""
Application's and its environment's configuration.
"""

import os

from sqlalchemy import URL, AsyncAdaptedQueuePool, NullPool


def _split_method_path(method_path: str) -> tuple[str, str]:
    """Split method and path from a string.
    This function takes a string in the format "METHOD:PATH" and splits it into
    a tuple containing the method and the path.
    For example, "GET:/api/v1/resource" will return ("GET", "/api/v1/resource").

    Args:
        method_path (str): The string to split.
    Returns:
        tuple[str, str]: The method and path.
    Raises:
        ValueError: If the string is not in the correct format.
    """
    if not method_path.strip():
        raise ValueError("Empty string provided")
    parts = method_path.split(":")
    if len(parts) != 2:
        raise ValueError(
            f"Invalid format: {method_path}. Expected format: 'METHOD:PATH'"
            f" (e.g. 'GET:/api/v1/resource')"
        )
    return tuple(parts)


def _split_method_path_list_string(
    method_path: str,
) -> tuple[tuple[str, str]]:
    """Split a comma-separated string of method and path pairs.
    This function takes a string where each pair is separated by a comma,
    and each pair consists of a method and a path separated by a colon.
    For example, "GET:/api/v1/resource,POST:/api/v1/resource".
    It returns a tuple of tuples, where each inner tuple contains the method and path.

    Args:
        method_path (str): The string to split.
    Returns:
        tuple[tuple[str, str]]: The method and path.
    Raises:
        ValueError: If the string is not in the correct format.
    """
    if not method_path.strip():
        return []
    if not isinstance(method_path, str):
        raise ValueError(f"Invalid type: {type(method_path)}. Expected type: str")
    return tuple(_split_method_path(url.strip()) for url in method_path.split(","))


class DatabaseConfig:
    """Database configuration."""

    DATABASE_DRIVERNAME = os.getenv("DATABASE_DRIVERNAME", "postgresql+asyncpg")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")
    POSTGRES_URI = (
        f"{DATABASE_DRIVERNAME}:"
        f"//{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )
    DB_URL = URL(
        drivername=DATABASE_DRIVERNAME,
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DATABASE,
        query={},
    )
    POSTGRES_ECHO = os.getenv("POSTGRES_ECHO", "false").lower() == "true"
    POOL_PRE_PING = os.getenv("POOL_PRE_PING", True)
    POOL_SIZE = int(os.getenv("POOL_SIZE", 5))
    MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW", 10))

    DATABASE_ENABLE_CONNECTION_POOLING = (
        os.getenv("DATABASE_ENABLE_CONNECTION_POOLING", "true").lower() == "true"
    )

    _POOLING_ARGS = (
        {
            "poolclass": AsyncAdaptedQueuePool,
            "pool_size": POOL_SIZE,
            "max_overflow": MAX_OVERFLOW,
        }
        if DATABASE_ENABLE_CONNECTION_POOLING
        else {
            "poolclass": NullPool,
        }
    )

    ENGINE_ARGS = {
        "echo": POSTGRES_ECHO,
        "pool_pre_ping": POOL_PRE_PING,
        **_POOLING_ARGS,
    }


class AuthConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


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
    LOGGER_IGNORE_PATHS = _split_method_path_list_string(
        os.getenv("LOGGER_IGNORE_PATHS", "GET:/docs,GET:/openapi.json")
    )

    LOGGER_IGNORE_INPUT_BODY_PATHS = _split_method_path_list_string(
        os.getenv(
            "LOGGER_IGNORE_INPUT_BODY_PATHS",
            "POST:/user/register,PUT:/user/,POST:/auth/token",
        )
    )

    LOGGER_IGNORE_OUTPUT_BODY_PATHS = _split_method_path_list_string(
        os.getenv("LOGGER_IGNORE_OUTPUT_BODY_PATHS", "POST:/auth/token")
    )

    DATABASE: DatabaseConfig = DatabaseConfig()
    AUTH: AuthConfig = AuthConfig()


class TestConfig(Config):
    """Test configuration."""

    ENVIRONMENT = "test"
    TESTING = True
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
