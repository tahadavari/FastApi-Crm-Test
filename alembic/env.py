"""Alembic environment configuration."""

from __future__ import annotations

import asyncio
from logging.config import fileConfig
from os import environ

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from infrastructure.db.base import Base
from infrastructure.db.models import activity, customer, deal, task  # noqa: F401
from settings import get_settings

config = context.config
fileConfig(config.config_file_name)  # type: ignore[arg-type]
settings = get_settings()
config.set_main_option("sqlalchemy.url", environ.get("DATABASE_URL", settings.database_url))


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  # type: ignore[arg-type]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    if isinstance(connectable, AsyncEngine):
        async def async_run_migrations() -> None:
            async with connectable.connect() as connection:
                await connection.run_sync(do_run_migrations)

        asyncio.run(async_run_migrations())
    else:
        with connectable.connect() as connection:
            do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
