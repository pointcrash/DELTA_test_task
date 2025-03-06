"""create package_type table

Revision ID: 88c877e88603
Revises: 
Create Date: 2025-03-06 16:07:15.634992

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "88c877e88603"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "package_types",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_package_types")),
        sa.UniqueConstraint("name", name=op.f("uq_package_types_name")),
    )


def downgrade() -> None:
    op.drop_table("package_types")
