"""Modified Products table from category ID column to category

Revision ID: 3593cb4049ed
Revises: 
Create Date: 2025-09-14 23:08:52.226723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3593cb4049ed'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # modify column name
    op.alter_column(
        table_name="products",
        column_name="category_id",
        new_column_name="category",
        existing_type=sa.UUID()
    )

    # modify column type
    op.alter_column(
        table_name="products",
        column_name="category",
        type_=sa.String(length=100),
        existing_type=sa.UUID()
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        table_name="products",
        column_name="category",
        new_column_name="category_id",
        existing_type=sa.UUID()
    )

    # modify column type
    op.alter_column(
        table_name="products",
        column_name="category_id",
        type_=sa.UUID(),
        existing_type=sa.String(length=100)
    )
