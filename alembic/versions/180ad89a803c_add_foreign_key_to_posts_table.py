"""add foreign-key to posts table

Revision ID: 180ad89a803c
Revises: d991f5eb51b2
Create Date: 2023-12-17 20:53:55.221509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '180ad89a803c'
down_revision: Union[str, None] = 'd991f5eb51b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk",
                        source_table="posts",
                        referent_table="users",
                        local_cols=["owner_id"],
                        remote_cols=["id"],
                        ondelete="CASCADE"
                        )


def downgrade() -> None:
    op.drop_constraint(constraint_name="posts_users_fk", table_name="posts")
    op.drop_column(table_name="posts", column_name="owner_id")