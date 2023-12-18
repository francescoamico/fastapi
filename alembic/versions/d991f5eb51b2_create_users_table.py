"""create users table

Revision ID: d991f5eb51b2
Revises: 39edb2adbb0d
Create Date: 2023-12-17 20:46:52.073286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd991f5eb51b2'
down_revision: Union[str, None] = '39edb2adbb0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("email", sa.String(), unique=True, nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table(table_name="users")