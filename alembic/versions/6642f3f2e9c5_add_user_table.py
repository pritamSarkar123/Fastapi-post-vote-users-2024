"""add user table

Revision ID: 6642f3f2e9c5
Revises: 8c1a0e2e5eaf
Create Date: 2024-04-17 16:12:22.576279

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "6642f3f2e9c5"
down_revision = "8c1a0e2e5eaf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
