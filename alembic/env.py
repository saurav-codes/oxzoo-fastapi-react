import os
import sys

# env.py is loaded from the alembic/ dir; the repo root holds db.py/models.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from alembic import context
from sqlalchemy import engine_from_config, pool

from db import SQLALCHEMY_URL
from models import Base

config = context.config

# DATABASE_URL comes from the ox project env, with the local-dev fallback in db.py.
config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
