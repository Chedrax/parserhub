import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from parserhub.core.config import get_settings
from parserhub.db.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(fname=config.config_file_name)

# Load application settings from environment variables / .env.
settings = get_settings()

# SQLAlchemy metadata used by Alembic for autogenerate.
#
# All SQLAlchemy models inheriting from Base are registered
# in Base.metadata. Alembic uses this metadata to detect
# changes between the models and the database schema.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    """

    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Configure Alembic and run migrations using a database connection."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run Alembic migrations."""

    configuration = config.get_section(
        name=config.config_ini_section,
        default={},
    )

    # Use the same database URL as the application.
    # The URL comes from Pydantic Settings rather than alembic.ini.
    configuration["sqlalchemy.url"] = settings.database_url

    # Create an asynchronous SQLAlchemy engine.
    connectable = async_engine_from_config(
        configuration=configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Alembic's migration API is synchronous, so run it
        # through SQLAlchemy's async connection.
        await connection.run_sync(fn=do_run_migrations)

    # Dispose the temporary Alembic engine and its resources.
    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    asyncio.run(main=run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
