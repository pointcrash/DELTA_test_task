"""create packages table

Revision ID: f34026cdfacf
Revises: 88c877e88603
Create Date: 2025-03-06 19:23:07.370157

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f34026cdfacf"
down_revision: Union[str, None] = "88c877e88603"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "packages",
        sa.Column("session_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("weight", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("content_cost", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("delivery_cost", sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["package_types.id"],
            name=op.f("fk_packages_type_id_package_types"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_packages")),
    )
    op.create_index(
        op.f("ix_packages_session_id"),
        "packages",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_packages_session_id"), table_name="packages")
    op.drop_table("packages")
