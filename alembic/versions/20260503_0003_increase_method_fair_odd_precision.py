"""increase method fair odd precision

Revision ID: 20260503_0003
Revises: 20260503_0002
Create Date: 2026-05-03
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260503_0003"
down_revision: str | None = "20260503_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "methods",
        "fair_odd",
        existing_type=sa.Numeric(10, 4),
        type_=sa.Numeric(18, 10),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "methods",
        "fair_odd",
        existing_type=sa.Numeric(18, 10),
        type_=sa.Numeric(10, 4),
        existing_nullable=False,
    )
