"""add delivery_service_id to packages table

Revision ID: 38c67b5dd648
Revises: f34026cdfacf
Create Date: 2025-03-07 12:45:13.708907

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "38c67b5dd648"
down_revision: Union[str, None] = "f34026cdfacf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "packages",
        sa.Column("delivery_service_id", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("packages", "delivery_service_id")
