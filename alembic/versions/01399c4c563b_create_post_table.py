"""create post table

Revision ID: 01399c4c563b
Revises: 
Create Date: 2024-04-17 15:46:38.819032

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "01399c4c563b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("published", sa.Boolean(), server_default="TRUE", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("owner_id", sa.Integer(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
