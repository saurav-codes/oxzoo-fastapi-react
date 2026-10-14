import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ox injects DATABASE_URL from the postgres service; the fallback keeps local
# `uv run` usable on a dev machine.
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgres://postgres@127.0.0.1:5432/oxzoo_fastapi_react"
)
# SQLAlchemy reads postgresql:// as psycopg2; this app uses psycopg 3.
# The pattern takes postgres:// too, which an older ox agent provides.
SQLALCHEMY_URL = re.sub(r"^postgres(ql)?://", "postgresql+psycopg://", DATABASE_URL)

engine = create_engine(SQLALCHEMY_URL)
Session = sessionmaker(engine)
