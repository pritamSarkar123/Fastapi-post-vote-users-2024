"""add foreignkey in posts to user

Revision ID: 893d3c09db4b
Revises: 6642f3f2e9c5
Create Date: 2024-04-17 16:16:26.807072

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "893d3c09db4b"
down_revision = "6642f3f2e9c5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
        onupdate="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    pass
