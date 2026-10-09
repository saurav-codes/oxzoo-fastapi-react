import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ox injects DATABASE_URL from the postgres service; the fallback keeps local
# `uv run` usable on a dev machine.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgres://postgres@127.0.0.1:5432/oxzoo_fastapi_react"
)
# SQLAlchemy needs the postgresql+psycopg scheme; ox provides postgres://.
SQLALCHEMY_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

engine = create_engine(SQLALCHEMY_URL)
Session = sessionmaker(engine)
