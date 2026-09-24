"""create greeting_log

One row per /api/greeting hit; the id uses pgcrypto's gen_random_uuid(),
declared as a postgres extension in ox.toml.
"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    op.execute(
        """
        CREATE TABLE greeting_log (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            greeting text NOT NULL,
            created_at timestamptz NOT NULL DEFAULT now()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS greeting_log")
