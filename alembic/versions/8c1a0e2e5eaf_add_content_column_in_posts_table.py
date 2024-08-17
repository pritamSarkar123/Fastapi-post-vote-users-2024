"""add content column in posts table

Revision ID: 8c1a0e2e5eaf
Revises: 01399c4c563b
Create Date: 2024-04-17 15:54:25.499357

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "8c1a0e2e5eaf"
down_revision = "01399c4c563b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
